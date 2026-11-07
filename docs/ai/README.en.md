# Compatibility entry and agent resources

[中文](README.md) | English

This directory preserves existing links and machine-readable resources. New users should start with the [user documentation](../README.en.md) or [user guide](../user/README.en.md); library changes start with the [maintainer and agent directory](../development/README.en.md).

## Installation shortcut

For CPython 3.13 on Windows AMD64 or Linux glibc 2.28+ x86_64:

```shell
python -m pip install --index-url https://pypi.org/simple/ --only-binary=:all: py-skia-canvas==0.1.0a19
```

## Paths and responsibilities

- [INSTALL](INSTALL.en.md), the [usage reference](usage/README.en.md), [API](usage/API_REFERENCE.en.md), [gallery](usage/DEMOS.en.md) and [troubleshooting](usage/TROUBLESHOOTING.en.md) remain valid, maintained user documentation. Their paths preserve references and image provenance, without a duplicated source in the new directory.
- [development](development/README.en.md) contains detailed library-maintainer and agent rules. Application users do not need that workflow.
- [facts.json](facts.json) and [llms.txt](../../llms.txt) provide machine navigation. [VALIDATION](VALIDATION.en.md) and asset manifests preserve existing evidence, without implying new rendering or publication for this change.

The directory name `ai` does not make every page AI-only. New user guides belong in `docs/user`, and new maintainer navigation in `docs/development`; existing detailed references remain maintained in their single location.
