# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html), read for a Python library:
MAJOR when a caller has to change code, MINOR for a new capability that leaves callers untouched,
PATCH for a fix; while on 0.x, a change that breaks a caller bumps MINOR. Each entry opens with one
sentence saying what a caller does differently, and an item that breaks a caller starts with
`Breaking:`. What is not released yet gathers under `## [Unreleased]`, renamed at the release to
the version and its date.

## [Unreleased]

Started from the KaxaNuk Python Library Template 0.1.3: a Python library laid out like the KaxaNuk
Data Curator, with one example module, its test, its documentation and a workflow that publishes a
tag to PyPI.

### Added

- `src/kn_python_library_template/`: `__version__` and the public API in `__init__.py`;
  `exceptions.py`, the library's error; `example.py`, one function to replace.
- `tests/unit/example_test.py`: pytest, its cases parametrized and its error checked.
- `docs/source/`: Sphinx, MyST and the pydata theme; `.readthedocs.yml` builds it on Read the Docs.
- `.github/workflows/main.yml`: ruff, mypy and pytest on Python 3.12 to 3.14, the documentation
  and the build; a `vX.Y.Z` tag published to PyPI by trusted publishing, and a try on TestPyPI
  started by hand.
- `AGENTS.md`: Bloom Code named, the tests, the release, and the `## Next` table the KaxaNuk
  Researcher's `next` reads.
