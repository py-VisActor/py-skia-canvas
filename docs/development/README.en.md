# Maintainer and agent documentation

[中文](README.md) | English

For maintainers and AI agents modifying py-skia-canvas itself. Application developers should use the [user documentation](../README.en.md), without running these internal workflows.

## Rules and workflow

- [AGENTS.md](../../AGENTS.md): stable rules, authorization and work boundaries.
- [Development guide and full constraints](../ai/development/README.en.md): architecture, the unique core, provenance and thread ownership.
- [Complete development workflow](../ai/development/AUTONOMOUS_WORKFLOW.en.md) · [Commands](../ai/development/WORKFLOW.en.md) · [Machine policy](../ai/development/workflow.json).
- [Documentation contract](../ai/development/DOCUMENTATION.en.md): bilingual pages, examples, audience separation and package description.
- [Testing and release](../ai/development/TESTING_AND_RELEASE.en.md) · [Release workflow](../RELEASE_WORKFLOW.md) · [Test tools](../../tests/README.md).
- [API compatibility rules](../API_COMPATIBILITY.md) · [Python host profile](../PYTHON_HOST_PROFILE.md).

## Status, sources and history

[Release records](../RELEASE_STATUS.md) describe public publication facts; the [reference directory](../../references/README.md) records pinned upstream sources and licenses. The [implementation plan](../IMPLEMENTATION_PLAN.md), [task list](../TASKS.md), [session handoff](../NEW_SESSION.md) and [migration report](../COMPLETION_REPORT.md) preserve development history. Check each document's date and applicable version.

`docs/ai/development` remains the single maintained source for detailed development rules. This directory provides the formal maintainer navigation without duplicating those rules. `docs/ai/usage` and `INSTALL` remain valid user references, not deprecated historical pages. Original validation reports, images and provenance hashes are unchanged.

## Documentation inventory

The [per-document audience inventory](documentation-inventory.json) separates user guidance, repository development, archives, evidence and legal notices. Retained paths keep their source context; classification does not turn historical acceptance into a current compatibility claim.
