import os
from pathlib import Path

import pytest
from mypy import api

TESTS_DIR = Path(__file__).parent


def gen_file_list():
    """List of all files included in the directory tests for typing checking them"""
    for path in TESTS_DIR.glob("*.py"):
        if not path.name.startswith("test_") and not path.name.startswith('X'):
            yield path


@pytest.mark.parametrize(
    "filepath",
    list(gen_file_list()),
    ids=[v.relative_to(TESTS_DIR).as_posix() for v in gen_file_list()],
)
def test_stubs(filepath: Path) -> None:
    """Run mypy over example files."""
    stdout, stderr, exitcode = api.run([os.fspath(filepath)])
    if stdout:
        print(stdout)
    if stderr:
        print(stderr)

    assert stdout.startswith("Success: no issues found")
    assert not stderr
    assert exitcode == 0


@pytest.mark.parametrize(
    "filepath", list(gen_file_list()), ids=[v.name for v in gen_file_list()]
)
def test_files(filepath):
    """Run the test files to make sure they work properly."""
    code = filepath.read_text(encoding="utf-8")
    exec(compile(code, filepath, "exec"), {})
