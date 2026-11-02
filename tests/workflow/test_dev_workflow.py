"""Negative/positive coverage tests for the development gate, never rendering acceptance."""
from pathlib import Path
import json
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
import dev_workflow as workflow
from validate_ai_docs import version_errors


class DevelopmentGateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        policy = workflow.load_policy(ROOT)
        paths = {p for group in policy['documentationTopics'].values() for p in group}
        for name in paths:
            self.put(name, '# Original\n')
        self.put(workflow.POLICY, json.dumps(policy))
        self.put('scripts/feature.py', 'VALUE = 1\n')
        self.put('.gitignore', 'test-runs/\n')
        workflow.git(self.root, 'init')
        workflow.git(self.root, 'add', '.')
        workflow.git(self.root, '-c', 'user.name=Workflow Test', '-c', 'user.email=test@example.invalid', 'commit', '-m', 'fixture')

    def put(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')

    def record(self, action='updated'):
        self.put('scripts/feature.py', 'VALUE = 2\n')
        docs = ['docs/ai/development/README.md', 'docs/ai/development/README.en.md']
        if action == 'updated':
            for name in docs:
                self.put(name, '# Updated guide\n')
        workflow.plan(self.root, 'HEAD', 'tooling', ['tooling'], 'Exercise the documentation and source coverage gate.', 'docs/changes/test.json')
        path = self.root / 'docs/changes/test.json'
        record = json.loads(path.read_text(encoding='utf-8'))
        record['acceptanceCriteria'] = ['Changed tooling requires bilingual documentation and actual scoped check reports.']
        record['documentation'] = [dict(topic='development', action=action, paths=docs, reason='The developer workflow documents the changed tooling and its limits.')]
        for row in record['checks']:
            report = self.root / f'test-runs/unit/{row["id"]}.json'
            status = {'source': 'SOURCE_CHECKS_PASSED', 'docs': 'AI_DOCS_STRUCTURALLY_VALIDATED', 'tooling_tests': 'TESTS_PASSED'}[row['id']]
            workflow.write_json(report, dict(status=status, fixtureOnly=True, _workflow=dict(sourceHashes=record['sources'], documentationHashes=workflow.documentation_hashes(self.root))))
            row.update(status='passed', command=['python', 'unit-fixture'], report=report.relative_to(self.root).as_posix(), sha256=workflow.digest(report))
        self.save(record)
        return record

    def save(self, record):
        self.put('docs/changes/test.json', json.dumps(record))

    def check(self, local=False):
        return workflow.check(self.root, 'HEAD', local)

    def test_docs_only_change_needs_no_native_record(self):
        self.put('README.md', '# Documentation edit\n')
        result = self.check()
        self.assertEqual(result['status'], 'CHANGE_COVERAGE_CHECKED')
        self.assertEqual(result['sourceFiles'], 0)

    def test_source_change_without_documentation_record_fails(self):
        self.put('scripts/feature.py', 'VALUE = 2\n')
        self.assertEqual(self.check()['status'], 'INCOMPLETE')

    def test_pending_plan_does_not_count_as_done(self):
        self.put('scripts/feature.py', 'VALUE = 2\n')
        workflow.plan(self.root, 'HEAD', 'tooling', ['tooling'], 'Incomplete task fixture.', 'docs/changes/test.json')
        self.assertEqual(self.check()['status'], 'INCOMPLETE')

    def test_record_only_success_is_not_rendering_acceptance(self):
        self.record()
        result = self.check()
        self.assertEqual(result['status'], 'CHANGE_COVERAGE_CHECKED')
        self.assertEqual(result['evidenceMode'], 'record-only')
        self.assertIn('not full API', result['limitation'])

    def test_local_evidence_hashes_and_context_pass(self):
        self.record()
        self.assertEqual(self.check(True)['status'], 'CHANGE_COVERAGE_CHECKED')

    def test_handoff_after_commit_uses_the_original_task_doc_scope(self):
        record = self.record()
        workflow.git(self.root, 'add', '.')
        workflow.git(self.root, '-c', 'user.name=Workflow Test', '-c', 'user.email=test@example.invalid', 'commit', '-m', 'completed task')
        record['nextStep'] = 'Handoff updated after the implementation commit.'
        self.save(record)
        self.assertEqual(self.check()['status'], 'CHANGE_COVERAGE_CHECKED')

    def test_missing_english_update_fails(self):
        record = self.record()
        record['documentation'][0]['paths'] = ['docs/ai/development/README.md']
        self.save(record)
        self.assertEqual(self.check()['status'], 'INCOMPLETE')

    def test_unchanged_docs_need_review_but_not_a_fake_edit(self):
        self.record('unchanged')
        self.assertEqual(self.check()['status'], 'CHANGE_COVERAGE_CHECKED')

    def test_empty_unchanged_reason_fails(self):
        record = self.record('unchanged')
        record['documentation'][0]['reason'] = ''
        self.save(record)
        self.assertEqual(self.check()['status'], 'INCOMPLETE')

    def test_source_edit_after_record_fails_coverage(self):
        self.record()
        self.put('scripts/feature.py', 'VALUE = 3\n')
        self.assertEqual(self.check()['status'], 'INCOMPLETE')

    def test_refresh_preserves_old_checks_without_reusing_them(self):
        self.record()
        self.put('scripts/feature.py', 'VALUE = 3\n')
        workflow.refresh_record(self.root, 'docs/changes/test.json')
        record = json.loads((self.root / 'docs/changes/test.json').read_text())
        self.assertEqual(record['checks'][0]['status'], 'not_run')
        self.assertEqual(record['previousChecks'][0]['checks'][0]['status'], 'passed')
        self.assertEqual(self.check()['status'], 'INCOMPLETE')

    def test_production_edit_cannot_hide_as_tooling(self):
        self.put('python/py_skia_canvas/new.py', 'VALUE = 1\n')
        self.record()
        self.assertEqual(self.check()['status'], 'INCOMPLETE')

    def test_script_edit_cannot_hide_as_documentation_only(self):
        record = self.record()
        record['kind'] = 'documentation'
        self.save(record)
        result = self.check()
        self.assertTrue(any('documentation-only' in error for row in result['records'] for error in row['errors']))

    def test_changed_local_artifact_fails(self):
        record = self.record()
        self.put(record['checks'][0]['report'], '{"status":"INCOMPLETE"}\n')
        self.assertEqual(self.check(True)['status'], 'INCOMPLETE')

    def test_attach_refuses_a_failed_report(self):
        self.record()
        self.put('test-runs/failed.json', '{"status":"INCOMPLETE"}')
        with self.assertRaises(ValueError):
            workflow.attach_report(self.root, 'docs/changes/test.json', 'source', 'test-runs/failed.json', ['python', 'fixture'])

    def test_non_source_checks_reject_failure_and_skip_statuses(self):
        record = self.record()
        record['checks'].append(dict(id='gpu', status='not_run'))
        self.save(record)
        for status in ('FAILED', 'ERROR', 'GPU_CHECK_FAILED', 'SKIPPED', 'NOT_RUN', 'TIMEOUT', 'BLOCKED', 'NOT_ACCEPTED', '', None, True):
            with self.subTest(status=status):
                workflow.write_json(self.root / 'test-runs/negative.json', dict(status=status))
                with self.assertRaisesRegex(ValueError, 'Unsuccessful evidence status'):
                    workflow.attach_report(self.root, 'docs/changes/test.json', 'gpu', 'test-runs/negative.json', ['python', 'actual-gpu-check'])
                (self.root / 'test-runs/negative.json').unlink()

    def test_docs_edit_after_test_requires_fresh_doc_evidence(self):
        self.record()
        self.put('docs/ai/development/README.md', '# Later edit\n')
        self.assertEqual(self.check(True)['status'], 'INCOMPLETE')

    def test_packaged_description_edit_invalidates_documentation_evidence(self):
        self.put('docs/PYPI_DESCRIPTION.md', '# Original package description\n')
        self.record()
        self.put('docs/PYPI_DESCRIPTION.md', '# Changed after documentation check\n')
        self.assertEqual(self.check(True)['status'], 'INCOMPLETE')

    def test_evidence_traversal_fails(self):
        record = self.record()
        record['checks'][0]['report'] = '../outside.json'
        self.save(record)
        self.assertEqual(self.check()['status'], 'INCOMPLETE')

    def test_read_only_snapshot_edit_fails_even_without_source_record(self):
        self.put('references/upstream/file.rs', '// edited\n')
        self.assertEqual(self.check()['status'], 'INCOMPLETE')

    def test_unicode_space_paths_are_not_split(self):
        self.put('scripts/含 空格.py', 'VALUE = 1\n')
        self.record()
        self.assertEqual(self.check()['status'], 'CHANGE_COVERAGE_CHECKED')

    def test_plan_refuses_existing_record(self):
        self.record()
        with self.assertRaises(FileExistsError):
            workflow.plan(self.root, 'HEAD', 'tooling', ['tooling'], 'Do not overwrite.', 'docs/changes/test.json')

    def test_event_cannot_supply_an_arbitrary_git_argument(self):
        self.put('event.json', '{"before":"--help"}')
        with self.assertRaises(ValueError):
            workflow.event_base(self.root, self.root / 'event.json')

    def test_runner_keeps_failure_logs_and_rejects_reuse(self):
        def command(args, **kwargs):
            failed = 'scripts/validate_core.py' in args
            output = b'{"status":"AI_DOCS_STRUCTURALLY_VALIDATED"}' if 'scripts/validate_ai_docs.py' in args else b'fixture log'
            return subprocess.CompletedProcess(args, 1 if failed else 0, output, b'')
        destination = self.root / 'test-runs/source'
        with patch.object(workflow, 'changed_files', return_value=('0'*40, [])), patch.object(workflow.subprocess, 'run', side_effect=command):
            result = workflow.run_source_checks(self.root, destination)
        self.assertEqual(result['status'], 'INCOMPLETE')
        self.assertTrue((destination / 'core.log').is_file())
        self.assertEqual(len((destination / 'commands.ndjson').read_text().splitlines()), 5)
        with self.assertRaises(FileExistsError):
            workflow.run_source_checks(self.root, destination)


class VersionPolicyTests(unittest.TestCase):
    def facts(self):
        return dict(version='0.1.0a18', sourceVersion='0.1.0a19', installation=dict(version='0.1.0a18', command='python -m pip install --index-url https://pypi.org/simple/ --only-binary=:all: py-skia-canvas==0.1.0a18'))

    def test_candidate_does_not_have_to_claim_it_is_published(self):
        self.assertEqual(version_errors(self.facts(), '0.1.0a19', '0.1.0a19'), [])

    def test_wrong_source_version_fails(self):
        self.assertTrue(version_errors(self.facts(), '0.1.0a18', '0.1.0a19'))

    def test_candidate_install_command_cannot_replace_published_command(self):
        facts = self.facts()
        facts['installation']['command'] = facts['installation']['command'].replace('a18', 'a19')
        self.assertTrue(version_errors(facts, '0.1.0a19', '0.1.0a19'))

    def test_cargo_prerelease_and_python_candidate_match(self):
        self.assertEqual(version_errors(self.facts(), '0.1.0a19', '0.1.0a19', '0.1.0-alpha.19', '0.1.0-alpha.19'), [])

    def test_stale_cargo_lock_is_not_a_matching_candidate(self):
        self.assertTrue(version_errors(self.facts(), '0.1.0a19', '0.1.0a19', '0.1.0-alpha.19', '0.1.0-alpha.18'))


if __name__ == '__main__':
    unittest.main()
