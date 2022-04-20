<img src="http://mypy-lang.org/static/mypy_light.svg" alt="mypy logo" width="300px"/>

# Mypy stubs for the PySide2 (Python for Qt5)

This repository holds the stubs of the *Qt5 for Python/PySide2* framework. The stubs are based on the stubs
which are delivered with the *Qt5 for python/PySide2*.

The work here takes heavy inspiration from the PyQt5-stubs and PyQt6-stubs projects.

The stubs are usable with any Qt5 for Python/PySide2 project. Please note that this work is far 
from complete. Don't hesitate to report problems or propose improvements.

# Installation

Simply install PySide2-stubs with pip:

    $ pip install PySide2-stubs

Or clone the latest version from Github and install it via Python setuptools:

    $ git clone https://github.com/bluebird75/PySide2-stubs
    $ python setup.py install


# Help improve the stubs

If you notice a incorrect typing information (mypy reports errors eventhough your code is correct), please report it
here with the following steps:

* create an issue showing your problem
* even better, create a PR to fix the problem
    * make sure to add a test showing what is mistyped. Just create a file under tests/ , not starting with test. The
      test suite will run the file and type-check it.
    * fix the stubs in the PySide2-stubs directory
    * and open the PR


