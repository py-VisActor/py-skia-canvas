# AI development workflow audit

[中文](WORKFLOW_AUDIT.md) | English

Audit date: 2026-10-29. Scope: AGENTS/startup material, AI development guides, build/capture/comparison/font/CPU/publication tools, and source CI. Conclusion: **AI has a complete execution path within fixed 3.0.8 compatibility, available resources, and current external authorization. This cannot guarantee unattended, exhaustive success for arbitrary features in arbitrary environments.**

## 1. Findings and changes

| Finding | Change in this batch | Remaining distinction |
| --- | --- | --- |
| Scattered instructions without unified starting/completion criteria | AUTONOMOUS_WORKFLOW, machine workflow.json, init plans/acceptance criteria | AI must understand requirements and choose semantic impact |
| Documentation was an end-of-task suggestion | AGENTS requires same-batch docs; topic mapping, change records, CI coverage | Structural checks cannot establish factual prose accuracy |
| English/demos/images/install facts were easy to omit | DOCUMENTATION defines triggers and bilingual/image/version requirements; unified run includes checks | Images/translations need actual semantic review |
| Source candidate coupled to public installation version | Separate sourceVersion, installation.version, acceptedWheels.version | Public baseline switches still require review and actual index checks |
| Upload-time PyPI README misled AI | Read-only candidate metadata gate and actual-description release checks | Existing release metadata cannot be rewritten; preserve accepted wheels |
| Old checks could be reused after edits | Source hash coverage, refresh invalidation, local artifact/source/doc context checks | Complex native reports still need actual object/scope review |
| No unified failure/recovery entry | Per-command logs/exit codes, source-check timeouts, fresh runs, previousChecks/nextStep | Interrupted incomplete runs are not passes; restart into new evidence |
| CI did not link code and documentation | Full-history checkout; PR-base/push-before coverage gate | Hosted CI cannot independently recreate local GPU/font evidence |
| GPU/CPU/fonts/GUI/publication could be conflated | Minimum checks by area/kind, retained full release gates | Area selection is developer review, not a full-API coverage proof |
| Extensions could silently exceed pinned behavior | Explicit user compatibility decision for extension; no tooling label for production edits | Record text grants no authorization or permission to replace algorithms |

## 2. Work AI can perform independently

| Stage | Execution | Checkable result |
| --- | --- | --- |
| Start/requirements/impact | Git state, init, criteria, areas/doc topics | Frozen base, pending checks, existing user edits |
| Reproduction/implementation | Original A/old wheel, independent assertions, shared-core/binding edits | Before/after behavior and source mapping |
| Build/install | Existing Windows/manylinux scripts, isolation | Actual candidate/hash, no Node/workspace dependencies |
| Functional verification | Capture/compare, CPU matrix, lifecycle, native/font tools | Exact results by mode/platform/backend and actual resources |
| Documentation/images | Bilingual edits, actual demos, manifests, description checks | Runnable instructions, visible output/provenance |
| Final review | run, attach, check --verify-evidence, diff/visual review | Original reports, source/doc hashes, complete handoff |
| External delivery | GitHub/index CLIs within authorization, independent downloads | Actual commits/runs/releases/index states |

Tools automate repeatable checks and record handling. AI still reasons, implements, diagnoses failures, and selects CLIs. This is not a one-click arbitrary-feature generator without AI decisions.

## 3. Conditions documentation cannot remove

Target GPUs/drivers, fonts/rights, GUI desktops, genuinely loader-less deployment environments, and necessary account access must exist. Software Vulkan is distinct from CPU Raster; driver blocking differs from absence of the library. Missing conditions remain unaccepted while independent work proceeds.

Changes to defaults, compatibility baseline, platform scope, or drawing algorithms require a current user decision. Existing authorization persists and should not be requested repeatedly. A record file cannot grant authorization for external publication.

Comprehensive feature confidence comes from contracts, regressions, exact A comparisons, real resources, lifecycles, and release matrices together. Tests/reviews can still miss unanticipated cases; `CHANGE_COVERAGE_CHECKED` or absence of failure cannot imply unconditional correctness.

## 4. Verification and acceptance scope for this batch

Workflow tests use temporary Git repositories to cover missing records, pending plans, missing English, unexplained unchanged docs, stale source/docs/artifacts, production misclassification, path traversal, read-only snapshots, Unicode paths, invalidated checks, and failure logs. Version tests cover simultaneous a19 candidate/a18 installation. Metadata tests cover stale publication language, local-only installation, wrong versions, and broken links.

This batch changes development process/docs/checkers. It uses tooling-scoped source/tool/bilingual checks, without rebuilding production or presenting historical GPU/CPU results as new feature acceptance. See the [change record](../../changes/20261029-ai-development-workflow.json); raw evidence is in `test-runs/20261029-ai-workflow-1/`.

## 5. Future use

The 2026-11-02 release review found that native checks without a dedicated success-status allowlist could accept a `FAILED` report. The gate now rejects failure, error, not-run, skipped, timeout, blocked and other negative statuses, as well as non-string statuses, with regression coverage. Status validation still does not replace reviewing raw results and the actual comparison targets.

Execute new tasks through [AUTONOMOUS_WORKFLOW](AUTONOMOUS_WORKFLOW.en.md) and deliver docs through [DOCUMENTATION](DOCUMENTATION.en.md). Preserve actual gaps and recovery steps. Configure platform paths/resources before tasks and verify affected behavior. More unattended operation needs continuously available GPU/GUI/loader-less runners and controlled account environments, rather than additional procedural text alone.
