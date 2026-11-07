# 0.1.0a20 release notes

[中文](RELEASE_NOTES_0.1.0a20.md) | English

This documentation and package-metadata revision does not change Canvas drawing, fonts, encoding, default backends or runtime dependencies. Actual publication and platform verification status is recorded in [release status](RELEASE_STATUS.md).

- Bilingual READMEs and the PyPI description focus on installation, a minimal example and usage limitations.
- [User documentation](README.en.md), the [user guide](user/README.en.md) and [maintainer directory](development/README.en.md) are separate. Existing `docs/ai` API references remain maintained and existing links remain valid.
- Project links use the current `py-VisActor/py-skia-canvas` repository. Documentation points to the user directory.
- AGENTS rules follow six sections covering responsibilities, starting work, repository structure, commands, modification constraints and verification.

The version remains alpha. Supported targets are CPython 3.13, Windows AMD64 and Linux glibc 2.28+ x86_64; other ABIs/platforms are outside the release matrix. Font behavior, thread ownership, GPU requirements for windows and the Windows parallel vector-file sequence limitation are unchanged; see the [user guide](user/README.en.md).
