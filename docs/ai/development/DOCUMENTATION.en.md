# Documentation, examples, and release-description delivery

[中文](DOCUMENTATION.md) | English

Documentation is part of feature delivery. When AI adds behavior, fixes bugs, or changes arguments/errors, builds/platforms, or developer tools, assess documentation impact first, update affected material, then run final checks. The [complete workflow](AUTONOMOUS_WORKFLOW.en.md) and [workflow.json](workflow.json) define execution and records.

Separate audiences: root READMEs and the PyPI description serve library users, covering installation, a minimal example, capabilities/limits and user links. The formal user entries are [docs/README](../../README.en.md) and [docs/user](../../user/README.en.md); maintainers and agents start at [docs/development](../../development/README.en.md). `docs/ai/usage` and INSTALL remain valid single-source references at their existing paths, preserving links and image provenance. Keep session notes, plans, acceptance and local reports in developer/evidence entries; do not rewrite historical evidence.

## 1. Update by impact

| Topic | Triggers | Material to review |
| --- | --- | --- |
| entry | Installation, capabilities/limitations, entry points, version status | Bilingual root/AI READMEs, llms.txt, facts.json |
| installation | ABI/platform/dependency/index/deployment changes | Bilingual INSTALL, public command, support matrix |
| api | Exports, signatures, defaults, units, returns, errors/ownership | Bilingual API_REFERENCE, source contracts, relevant ledger/status |
| usage | Calls, behavior, failures, thread/async changes | Bilingual usage README/TROUBLESHOOTING |
| demos | New visible graphics/text/export/window capabilities | Runnable code, bilingual DEMOS/example README, affected images/manifest |
| development | Tools, dependencies, builds, verification, recovery, CI | Bilingual development guide, WORKFLOW, acceptance and this process |
| release | Candidate/acceptance/index state, versions, package metadata | RELEASE_STATUS, facts, wheel description, release evidence |

Actual paths are in machine policy. Choose `updated` or `unchanged` with specific reasons and reviewed paths. Updated paths must appear in Git differences; paired docs include both languages. Unchanged reviews explain why actual behavior, signature, and usage need no update. “Checked” or “no impact” alone is insufficient.

A fix restoring already documented behavior may leave prose unchanged with a recorded review. Public extensions must update API/usage docs. Missing impact analysis does not justify skipping documentation.

## 2. Method-level contracts

Each new/migrated entry documents:

- Purpose and valid input, including omission, undefined/null, and overloads.
- Units, defaults, numeric/string boundaries, and read/conversion order.
- Return value/type, synchronous/awaitable behavior, call-time snapshots.
- Error conditions, ignored-invalid-input/STRICT behavior, failure side effects.
- Creation thread, ownership, parent/child lifetimes, transferable data.
- Pinned upstream location, shared-core call, relevant scenes/assertions.

Use the same public names as implementation. Do not copy browser Canvas or another Python library's defaults. Describe bug triggers and before/after outcomes concretely.

## 3. Languages, examples, and images

Chinese retains existing paths, English uses `.en.md`, and pages link reciprocally. Example code, CLI arguments, and image references agree; both languages fully explain limitations. Machine policy/JSON facts are shared. Do not rewrite historical evidence merely to translate it.

Execute new/affected demos against the actual candidate/installed wheel, inspect dimensions/pixels/metrics/backend, then copy original PNG bytes to stable assets. Preserve version, wheel/script/output hashes, and original run; update manifest and both galleries' descriptions/alt text. Prose-only edits need no rerendering. Unaffected images retain original provenance rather than being relabeled as new-candidate output.

`validate_ai_docs.py` checks local links, routes, heading structure, Python AST/command agreement, public exports, version facts, and image provenance. Syntax/link success does not establish translation semantics, visual approval, or accurate user explanations. AI must still review behavior.

## 4. Source candidate, public release, and image baseline

| Field/material | Meaning | Update timing |
| --- | --- | --- |
| pyproject / Python / crate / lock | Source candidate | Coordinate implementation/new-release preparation |
| `facts.sourceVersion` | Candidate matching source | Update with pyproject/Python |
| `facts.version`, `installation.version` | Public documentation/install release | Update together when explicitly switching the public baseline |
| `installation.publishedToPyPI` / release records | Actual index state | Update after querying/verifying publication, never inferred from CI |
| `acceptedWheels.version`, assets manifest | Accepted implementation behind images | Update after actual outputs/provenance exist |

For example, with a18 published and a19 in source, installation may remain pinned to `0.1.0a18` while sourceVersion is `0.1.0a19`. Mark candidate APIs with their applicable/unreleased version so old-wheel users do not copy unavailable entries. Never label candidates published or relabel old images merely to satisfy a checker.

## 5. Inspect the actual wheel description before upload

The `readme` field in `pyproject.toml` selects `docs/PYPI_DESCRIPTION.md`, an independent English release description with absolute links. The bilingual root READMEs retain repository navigation and current installation status. Documentation validation also checks code and links in the actual packaged description; reviewing only the root README is insufficient.

PyPI descriptions come from upload-time METADATA and do not follow GitHub README changes. New releases use neutral installation/capability language. Volatile “not yet published” claims become permanently stale; publication progress belongs in RELEASE_STATUS. PyPI documentation/image links must work independently of repository-relative paths, with an absolute Documentation project URL.

Fix descriptions, links, and versions in source before building. Replace the placeholder wheel/version, then check the actual candidate:

```shell
python scripts/check_package_metadata.py dist/NEW_CANDIDATE.whl --version NEW_VERSION --out test-runs/NEW_METADATA/report.json
```

The tool reads wheel metadata to check name/version/Python range, installation, stale publication claims, and links. It changes no accepted wheel and replaces no native/install tests. Historical a18 artifacts may fail this new quality gate due to their old README. Record the limitation and retain original bytes; never modify them and claim identical acceptance.

After description checks, accept the same wheel in actual tests, then freeze/publish it. Query index version/description/file hashes after upload. Incorrect content requires a new version, not deleting/reuploading old files or placeholder artifacts.

## 6. Documentation completion review

1. Entry-page readers can find applicable version, production-index command, and ABI/platform requirements.
2. Signatures, units, defaults, errors, and thread constraints match implementation.
3. New/changed workflows have runnable examples and actual output without fabricated/stale image or code labels.
4. Both languages communicate all limits with matching code/commands.
5. Public install version, source candidate, image baseline, and index state are separately accurate.
6. Task records resolve documentation impact; final documentation checks follow the last edit.
7. For authorized synchronization, verify public GitHub content. For publication, verify actual PyPI content. Old search cache is not proof of propagation.

Attach actual evidence and verify locally as in [AUTONOMOUS_WORKFLOW](AUTONOMOUS_WORKFLOW.en.md).
