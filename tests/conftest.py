"""
What every test shares: the package's scripts and tools/ on the import path, as each script puts its
own folder there when it runs, so a test imports one by its name, `import scaffold`.
"""
import pathlib
import sys

__all__ = []

REPOSITORY = pathlib.Path(__file__).resolve().parent.parent

for script_folder in [
    *sorted(REPOSITORY.glob('.apm/skills/*/scripts')),
    REPOSITORY / 'tools',
]:
    if str(script_folder) not in sys.path:
        sys.path.insert(0, str(script_folder))
