"""Plan changes, run local source checks, and enforce documentation/evidence coverage.

Development tooling only; no renderer or native objects. CI checks records and
hashes; --verify-evidence additionally reads local evidence. Neither mode grants
release acceptance or authorization for external actions.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
import fnmatch
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
POLICY = 'docs/ai/development/workflow.json'
RECORD_SCHEMA = 'py-skia-canvas-change-record/v1'


def git(root, *args):
    """Return Git output bytes or raise on failure; argv only, no shell/graphics."""
    return subprocess.run(['git', '-C', str(root), *args], check=True, capture_output=True).stdout


def local_path(root, name):
    """Resolve a repository-relative path, rejecting traversal/symlink escape; ValueError."""
    if not isinstance(name, str):
        raise ValueError('Repository path must be a string')
    parts = PurePosixPath(name)
    if not name or '\\' in name or parts.is_absolute() or '..' in parts.parts or ':' in name:
        raise ValueError(f'Unsafe repository path: {name}')
    result = (root / name).resolve()
    if not result.is_relative_to(root.resolve()):
        raise ValueError(f'Path escapes repository: {name}')
    return result


def digest(path):
    """Return SHA256 of file bytes, or None for a deleted file; no native ownership."""
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None


def matches(name, patterns):
    """Match normalized Git paths against policy patterns; bool, no side effects."""
    return any(fnmatch.fnmatchcase(name, pattern) for pattern in patterns)


def changed_files(root, base):
    """Include tracked edits/deletions and nonignored new files against a real commit."""
    if not base or base.startswith('-'):
        raise ValueError('Invalid base revision')
    commit = git(root, 'rev-parse', '--verify', base + '^{commit}').decode().strip()
    tracked = git(root, 'diff', '--name-only', '--no-renames', '-z', commit, '--')
    new = git(root, 'ls-files', '--others', '--exclude-standard', '-z')
    return commit, sorted({os.fsdecode(p) for p in (tracked + new).split(b'\0') if p})


def requirements(policy, kind, areas):
    """Return required check IDs/doc topics; unknown task scope raises ValueError."""
    if kind not in policy['kinds'] or not areas or any(a not in policy['areas'] for a in areas):
        raise ValueError('Unknown kind/areas or missing areas')
    scopes = [policy['kinds'][kind], *(policy['areas'][a] for a in areas)]
    return sorted({x for s in scopes for x in s['checks']}), sorted({x for s in scopes for x in s['documentation']})


def load_policy(root):
    """Read the machine-readable development policy; schema errors are explicit."""
    policy = json.loads((root / POLICY).read_text(encoding='utf-8'))
    if policy.get('schema') != 'py-skia-canvas-development-workflow/v1':
        raise ValueError('Unsupported development workflow schema')
    return policy


def documentation_hashes(root):
    """Fingerprint project docs/images and package description, excluding task records."""
    paths = [*sorted((root / 'docs').rglob('*')), *root.glob('README*.md'), *(root / 'examples').glob('README*.md'), root / 'llms.txt']
    records = (root / 'docs/changes').resolve()
    return {p.relative_to(root).as_posix(): digest(p) for p in paths if p.is_file() and not p.resolve().is_relative_to(records)}


def plan(root, base, kind, areas, objective, record):
    """Create one new change record with pending checks; never claim work passed."""
    policy = load_policy(root)
    commit, changed = changed_files(root, base)
    checks, topics = requirements(policy, kind, areas)
    target = local_path(root, record)
    if target.parent != (root / policy['recordDirectory']).resolve() or not re.fullmatch(r'[a-z0-9][a-z0-9-]*\.json', target.name):
        raise ValueError('Record must be a fresh docs/changes/<slug>.json')
    result = dict(schema=RECORD_SCHEMA, id=target.stem, objective=objective, kind=kind, areas=areas, baseCommit=commit,
                  acceptanceCriteria=[], environment={}, decisions=[],
                  sources={p: digest(local_path(root, p)) for p in changed if matches(p, policy['sourcePatterns'])},
                  documentation=[dict(topic=t, action='pending', reason='', paths=policy['documentationTopics'][t]) for t in topics],
                  checks=[dict(id=c, status='not_run', command=[], report='', sha256='') for c in checks],
                  compatibilityDecision='', limitations=[], nextStep='Complete impact review and preserve before-change evidence.')
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open('x', encoding='utf-8') as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    return dict(status='CHANGE_PLANNED', record=record, requiredChecks=checks, requiredDocumentation=topics,
                scope='Pending plan only; no implementation or acceptance implied.')


def refresh_record(root, name):
    """Refresh source hashes and invalidate old check attestations, preserving history."""
    policy = load_policy(root)
    path = local_path(root, name)
    if path.parent != (root / policy['recordDirectory']).resolve():
        raise ValueError('Record must be under docs/changes')
    record = json.loads(path.read_text(encoding='utf-8'))
    if record.get('schema') != RECORD_SCHEMA:
        raise ValueError('Unsupported change record')
    _, changed = changed_files(root, record['baseCommit'])
    sources = {p: digest(local_path(root, p)) for p in changed if matches(p, policy['sourcePatterns'])}
    if sources != record['sources']:
        record.setdefault('previousChecks', []).append(dict(sources=record['sources'], checks=deepcopy(record['checks'])))
        record['sources'] = sources
        for row in record['checks']:
            row.update(status='not_run', report='', sha256='')
        path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return dict(status='SOURCE_HASHES_REFRESHED', sourceFiles=len(sources), scope='Changed source invalidates old check claims; original evidence files remain intact.')


def evidence_errors(root, policy, record, key, row):
    """Verify local report bytes/status/context; report semantics still need review."""
    errors = []
    path = local_path(root, row.get('report', ''))
    if not path.is_relative_to((root / 'test-runs').resolve()) or path.suffix != '.json':
        return [f'Evidence must be a JSON report under test-runs: {key}']
    if not path.is_file() or digest(path) != row['sha256']:
        return [f'Missing/changed local evidence: {key}']
    evidence = json.loads(path.read_text(encoding='utf-8'))
    accepted = policy.get('evidenceStatuses', {}).get(key)
    status = evidence.get('status', '')
    unsuccessful = (not isinstance(status, str) or not status.strip() or
                    bool(re.search(r'(?:^|_)(?:FAIL(?:ED|URE)?|ERROR|INCOMPLETE|DIFFERENT|SKIP(?:PED)?|NOT_RUN|TIMEOUT|BLOCKED|UNAVAILABLE|UNSUCCESSFUL|NOT_ACCEPTED)(?:_|$)', status, re.I)))
    if unsuccessful or (accepted and status not in accepted):
        errors.append(f'Unsuccessful evidence status: {key}: {status}')
    if key in ('source', 'docs', 'tooling_tests'):
        context = evidence.get('_workflow', {})
        if any(name not in context.get('sourceHashes', {}) or context['sourceHashes'][name] != sha for name, sha in record.get('sources', {}).items()):
            errors.append(f'Evidence predates the recorded source bytes: {key}')
        if key == 'docs' and context.get('documentationHashes') != documentation_hashes(root):
            errors.append('Documentation changed after its evidence was captured')
    return errors


def attach_report(root, name, key, report, command):
    """Attach an existing successful local report with its actual hash, never execute it."""
    policy = load_policy(root)
    path = local_path(root, name)
    if path.parent != (root / policy['recordDirectory']).resolve() or not command:
        raise ValueError('A task record and actual command argv are required')
    record = json.loads(path.read_text(encoding='utf-8'))
    row = next((r for r in record['checks'] if r['id'] == key), None)
    if row is None:
        raise ValueError('Check is not part of this task plan')
    candidate = dict(id=key, status='passed', command=command, report=report, sha256=digest(local_path(root, report)))
    errors = evidence_errors(root, policy, record, key, candidate)
    if errors:
        raise ValueError('; '.join(errors))
    row.update(candidate)
    path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return dict(status='EVIDENCE_ATTACHED', check=key, report=report, sha256=candidate['sha256'], scope='Report bytes verified; scoped semantics still require developer review.')


def check_record(root, policy, record, changed, verify_evidence):
    """Validate one review record; local mode checks evidence bytes/status, no rendering."""
    errors = []
    if record.get('schema') != RECORD_SCHEMA or not record.get('objective', '').strip():
        raise ValueError('Invalid change record schema/objective')
    if not re.fullmatch(r'[0-9a-f]{40}', record.get('baseCommit', '')):
        raise ValueError('Change record must freeze an exact base commit')
    _, task_changed = changed_files(root, record['baseCommit'])
    if not record.get('acceptanceCriteria') or any(not isinstance(s, str) or not s.strip() for s in record['acceptanceCriteria']):
        errors.append('Explicit acceptance criteria are required')
    kind = record['kind']
    checks, topics = requirements(policy, kind, record['areas'])
    sources = record.get('sources', {})
    if kind == 'documentation' and sources:
        errors.append('Executable/source edits cannot be classified as documentation-only')
    if kind in ('documentation', 'tooling') and any(matches(p, policy['productionPatterns']) for p in sources):
        errors.append('Production edits cannot be classified as documentation/tooling')
    if kind == 'extension' and len(record.get('compatibilityDecision', '').strip()) < 20:
        errors.append('Extension needs the explicit user compatibility decision and its scope')
    coverage = set()
    for name, sha in sources.items():
        if not matches(name, policy['sourcePatterns']):
            errors.append(f'Unrecognized source entry: {name}')
        elif digest(local_path(root, name)) == sha:
            coverage.add(name)
    docs = {item['topic']: item for item in record.get('documentation', [])}
    if len(docs) != len(record.get('documentation', [])):
        errors.append('Duplicate documentation topic')
    for topic in topics:
        row = docs.get(topic, {})
        paths = row.get('paths', [])
        if not paths or any(p not in policy['documentationTopics'][topic] or not local_path(root, p).is_file() for p in paths):
            errors.append(f'Missing/invalid documentation paths: {topic}')
        if len(row.get('reason', '').strip()) < 20:
            errors.append(f'Documentation review needs a concrete reason: {topic}')
        if row.get('action') == 'updated':
            if not paths or not all(p in task_changed for p in paths):
                errors.append(f'Documentation marked updated without matching changes: {topic}')
            for name in paths:
                if name.endswith('.md'):
                    other = name[:-6] + '.md' if name.endswith('.en.md') else name[:-3] + '.en.md'
                    if (root / other).exists() and other not in paths:
                        errors.append(f'Both documentation languages must be reviewed/updated: {name}')
        elif row.get('action') != 'unchanged':
            errors.append(f'Unfinished documentation review: {topic}')
        if kind == 'extension' and topic in ('api', 'usage') and row.get('action') != 'updated':
            errors.append(f'Public extensions require updated {topic} docs')
    results = {row['id']: row for row in record.get('checks', [])}
    if len(results) != len(record.get('checks', [])):
        errors.append('Duplicate check ID')
    for key in checks:
        row = results.get(key, {})
        if row.get('status') != 'passed' or not isinstance(row.get('command'), list) or not row['command'] or any(not isinstance(s, str) or not s for s in row['command']) or not re.fullmatch(r'[0-9a-f]{64}', row.get('sha256', '')):
            errors.append(f'Missing passed check/command/evidence hash: {key}')
            continue
        path = local_path(root, row.get('report', ''))
        if not path.is_relative_to((root / 'test-runs').resolve()) or path.suffix != '.json':
            errors.append(f'Evidence must be a JSON report under test-runs: {key}')
            continue
        if verify_evidence:
            errors += evidence_errors(root, policy, record, key, row)
    return coverage, errors


def check(root, base, verify_evidence=False):
    """Check changed-source coverage; CI mode cannot certify missing local artifacts."""
    policy = load_policy(root)
    commit, changed = changed_files(root, base)
    errors = [f'Read-only upstream snapshot changed: {p}' for p in changed if matches(p, policy['protectedPatterns'])]
    required = {p for p in changed if matches(p, policy['sourcePatterns'])}
    covered = set()
    records = []
    for name in changed:
        if name.startswith(policy['recordDirectory'] + '/') and name.endswith('.json') and (root / name).is_file():
            try:
                record = json.loads((root / name).read_text(encoding='utf-8'))
                coverage, issues = check_record(root, policy, record, changed, verify_evidence)
                records.append(dict(path=name, errors=issues, matchingSources=sorted(coverage)))
                if not issues:
                    covered |= coverage
            except (ValueError, KeyError, TypeError) as error:
                records.append(dict(path=name, errors=[str(error)], matchingSources=[]))
    missing = sorted(required - covered)
    if missing:
        errors.append('Source changes lack a valid documentation/check record: ' + ', '.join(missing))
    for row in records:
        errors += [row['path'] + ': ' + e for e in row['errors']]
    return dict(status='CHANGE_COVERAGE_CHECKED' if not errors else 'INCOMPLETE', baseCommit=commit, changedFiles=changed,
                sourceFiles=len(required), records=records, evidenceMode='local-bytes' if verify_evidence else 'record-only', errors=errors,
                limitation='Documentation and scoped evidence coverage only; not full API/GPU/CPU/visual/release acceptance. Area selection and semantic review remain developer responsibilities.')


def write_json(path, value):
    """Write a fresh UTF-8 JSON evidence file; refuses overwrites."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def run_source_checks(root, out, base='HEAD'):
    """Run repeatable source/doc/tool tests as isolated processes, recording all failures."""
    if not out.resolve().is_relative_to((root / 'test-runs').resolve()):
        raise ValueError('Source-check output must be a fresh directory under test-runs')
    out.mkdir(parents=True, exist_ok=False)
    policy = load_policy(root)
    commit, changed = changed_files(root, base)
    context = dict(baseCommit=commit, sourceHashes={p: digest(local_path(root, p)) for p in changed if matches(p, policy['sourcePatterns'])}, documentationHashes=documentation_hashes(root))
    commands = [('bootstrap', ['scripts/validate_bootstrap.py']), ('core', ['scripts/validate_core.py']),
                ('licenses', ['scripts/validate_licenses.py']), ('docs', ['scripts/validate_ai_docs.py']),
                ('tooling_tests', ['-m', 'unittest', 'discover', '-s', 'tests/workflow', '-v'])]
    checks = []
    for key, args in commands:
        argv = [sys.executable, *args]
        try:
            result = subprocess.run(argv, cwd=root, capture_output=True, timeout=300)
        except subprocess.TimeoutExpired as error:
            result = subprocess.CompletedProcess(argv, 124, error.stdout or b'', (error.stderr or b'') + b'\nSource check timed out\n')
        log = out / (key + '.log')
        log.write_bytes(result.stdout + result.stderr)
        row = dict(id=key, argv=argv, exitCode=result.returncode, log=log.name, logSha256=digest(log))
        checks.append(row)
        if key == 'docs' and result.returncode == 0:
            report = json.loads(result.stdout)
        else:
            report = dict(status=('TESTS_PASSED' if key == 'tooling_tests' else 'COMMAND_PASSED') if result.returncode == 0 else 'INCOMPLETE', **row)
        report['_workflow'] = context
        write_json(out / (key + '.json'), report)
        with (out / 'commands.ndjson').open('a', encoding='utf-8') as journal:
            journal.write(json.dumps(row) + '\n')
        print(key, result.returncode, flush=True)
    summary = dict(status='SOURCE_CHECKS_PASSED' if all(x['exitCode'] == 0 for x in checks) else 'INCOMPLETE', checks=checks, _workflow=context,
                   limitation='Source/doc/tool tests; no candidate wheel or rendering acceptance.')
    write_json(out / 'run.json', summary)
    return summary


def event_base(root, event_path):
    """Read GitHub event base SHA; initial/manual events use the parent commit."""
    event = json.loads(event_path.read_text(encoding='utf-8'))
    base = event.get('pull_request', {}).get('base', {}).get('sha') or event.get('before')
    if base and base != '0' * 40:
        if not re.fullmatch(r'[0-9a-f]{40}', base):
            raise ValueError('Invalid GitHub event base SHA')
        return base
    return git(root, 'rev-parse', 'HEAD^').decode().strip()


def main():
    """CLI: init/run/check; writes only explicit fresh task/evidence paths."""
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    init = sub.add_parser('init')
    init.add_argument('--base', default='HEAD')
    init.add_argument('--kind', required=True)
    init.add_argument('--areas', required=True)
    init.add_argument('--objective', required=True)
    init.add_argument('--record', required=True)
    run = sub.add_parser('run')
    run.add_argument('--out', type=Path, required=True)
    run.add_argument('--base', default='HEAD')
    run.add_argument('--record')
    refresh = sub.add_parser('refresh')
    refresh.add_argument('--record', required=True)
    attach = sub.add_parser('attach')
    attach.add_argument('--record', required=True)
    attach.add_argument('--id', required=True)
    attach.add_argument('--report', required=True)
    attach.add_argument('--command', nargs=argparse.REMAINDER, required=True)
    verify = sub.add_parser('check')
    verify.add_argument('--base', default='HEAD')
    verify.add_argument('--record')
    verify.add_argument('--event-file', type=Path)
    verify.add_argument('--verify-evidence', action='store_true')
    verify.add_argument('--out', type=Path)
    args = parser.parse_args()
    try:
        if args.action == 'init':
            result = plan(ROOT, args.base, args.kind, args.areas.split(','), args.objective, args.record)
        elif args.action == 'refresh':
            result = refresh_record(ROOT, args.record)
        elif args.action == 'attach':
            result = attach_report(ROOT, args.record, args.id, args.report, args.command)
        elif args.action == 'run':
            base = json.loads(local_path(ROOT, args.record).read_text(encoding='utf-8'))['baseCommit'] if args.record else args.base
            result = run_source_checks(ROOT, args.out, base)
        else:
            base = json.loads(local_path(ROOT, args.record).read_text(encoding='utf-8'))['baseCommit'] if args.record else args.base
            result = check(ROOT, event_base(ROOT, args.event_file) if args.event_file else base, args.verify_evidence)
            if args.out:
                write_json(args.out, result)
        visible = dict(status=result['status'], checks=len(result['checks']), report=str(args.out / 'run.json'), scope=result['limitation']) if args.action == 'run' else result
        print(json.dumps(visible, ensure_ascii=False, indent=2))
        raise SystemExit(1 if result['status'] == 'INCOMPLETE' else 0)
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError) as error:
        parser.exit(2, str(error) + '\n')


if __name__ == '__main__':
    main()
