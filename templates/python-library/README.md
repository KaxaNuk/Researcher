# KN Python Library Template

| |
|---|
| [![Python](https://img.shields.io/badge/python-3.12%20%7C%203.13%20%7C%203.14-blue?logo=python&logoColor=ffdd54)](https://www.python.org) [![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE) [![Build Status](https://github.com/github-owner/kn-python-library-template/actions/workflows/main.yml/badge.svg)](https://github.com/github-owner/kn-python-library-template/actions/workflows/main.yml) |

[One sentence on what the library does.]

> **Status: nothing released yet.** Replace this line as the library moves; it is the same line
> in `README.md` and `AGENTS.md`.

Laid out like the [KaxaNuk Data Curator](https://github.com/KaxaNuk/Data-Curator), KaxaNuk's
open-source Python library for financial data: the package in `src/`, its tests in `tests/`, its
documentation in `docs/` for Read the Docs, and one workflow that tests every push and publishes
each tagged version to PyPI. Started from the KaxaNuk Python Library Template, in the
[KaxaNuk Researcher](https://github.com/KaxaNuk/Researcher).

## Documentation

<https://kn-python-library-template.readthedocs.io/en/latest/>, once Read the Docs builds it.

## Requirements

Python 3.12 or newer.

## Installation

From PyPI, once a release is out:

```bash
pip install kn-python-library-template
```

## Usage

```python
import kn_python_library_template

kn_python_library_template.percentage_change(100.0, 110.0)  # 0.1
```

## Development

With [uv](https://docs.astral.sh/uv/), in this folder:

```bash
uv sync                  # Python, the library and every development tool, into .venv/
uv run pytest            # the tests
uv run ruff check .      # the linter
uv run mypy              # the type hints
uv run sphinx-build -W -b html docs/source docs/_build/html   # the documentation
uv build                 # the wheel and the source archive, into dist/
```

[`AGENTS.md`](AGENTS.md) says how work is done here: the style, the tests, the changelog and the
release.

## License

MIT; see [`LICENSE`](LICENSE).
