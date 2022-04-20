"""Script for installation with pip."""
from setuptools import setup  # type: ignore

from version import PYSIDE2_VERSION, STUB_VERSION

setup(
    name="PySide2-stubs",
    url="https://github.com/bluebird75/pyside2-stubs",
    author="Philippe Fremy",
    maintainer_email="phil.fremy@free.fr",
    description="PEP561 stub files for the PySide2/Qt5 for Python framework",
    version=".".join((str(nbr) for nbr in PYSIDE2_VERSION + (STUB_VERSION,))),
    python_requires=">= 3.6",
    package_data={"PySide2-stubs": ["*.pyi"]},
    packages=["PySide2-stubs"],
)
