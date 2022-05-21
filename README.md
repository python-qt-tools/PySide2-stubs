<img src="http://mypy-lang.org/static/mypy_light.svg" alt="mypy logo" width="300px"/>

[![CI](https://github.com/python-qt-tools/PySide2-stubs/actions/workflows/ci.yml/badge.svg)](https://github.com/python-qt-tools/PySide2-stubs/actions/workflows/ci.yml)


# Mypy stubs for the PySide2 (Qt5 for Python)

*Author :* Philippe Fremy (with inspiration from the [PyQt5-stubs project](https://github.com/python-qt-tools/PyQt5-stubs/))

If you want to use `mypy` with your `PySide2` project and found the official stubs to be of insufficient quality, 
you are at the right place. This project improves the official stubs delivered by [Qt5 for Python/PySide2](https://pypi.org/project/PySide2/).

### Improvements:
* fix Signal with method emit()
* fix qVersion() returning string, not bytes
* fix QMessageBox.warning, information, critical, question, about, aboutQt to accept None as parent argument
* fix QAction.setShortcut() to accept string as argument
* fix QTreeWidgetItem comparison with <
* fix QTimer.timeout undeclared signal
* fix QLineEdit.setText() to accept None

See [CHANGELOG.md](CHANGELOG.md) for more details.

Please note that this work is far from complete. Don't hesitate to report problems or propose improvements.


# Licensing
As a derived work from PySide2, the stubs are delivered under the LGPL v2.1 . See file LICENSE for more details.


# Installation

Simply install the official PySide2-stubs with pip:

    $ pip install PySide2-stubs

Or use the latest version from Github:

    $ pip install git+https://github.com/bluebird75/PySide2-stubs


That's it, in both cases, the new stubs are picked up automatically by `mypy`. Typechecking process should be much better.


# Help improve the stubs

If you notice incorrect or missing typing information (mypy reports errors eventhough your code is correct), please report it
here with the following steps:

* create an issue showing your problem
* even better, create a PR to fix the problem
    * make sure to add a test showing what is mistyped. Just create a file under `tests/` , with a name
      not starting with *test*. The test suite will run the file and type-check it.
    * fix the stubs in the PySide2-stubs directory
    * and open the PR


