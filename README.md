<img src="http://mypy-lang.org/static/mypy_light.svg" alt="mypy logo" width="300px"/>

[![CI](https://github.com/python-qt-tools/PySide2-stubs/actions/workflows/python-package.yml/badge.svg)](https://github.com/python-qt-tools/PySide2-stubs/actions/workflows/python-package.yml)


# Mypy stubs for the PySide2 (Qt5 for Python)

Maintainer: Philippe Fremy, with inspiration from the [PyQt5-stubs project](https://github.com/python-qt-tools/PyQt5-stubs/).

If you want to use `mypy` with your `PySide2` project and found the official stubs to be of insufficient quality, 
you are at the right place. This project improves significantly the official stubs delivered by [Qt for PySide2](https://pypi.org/project/PySide2/).
The work here takes heavy inspiration from the [PyQt5-stubs](https://github.com/python-qt-tools/PyQt5-stubs/) and [PyQt6-stubs](https://github.com/python-qt-tools/PyQt6-stubs/) projects.

Improvements include:
* fix Signal to make it accept method emit()
* fix qVersion() returning string, not bytes
* fix QMessageBox.warning, information, critical, question, about, aboutQt to accept None as parent argument
* fix QProgressDialog.setCancelButton() to accept None
* fix QTreeWidget.topLevelItem() returning possibly None
* fix QMessageBox.StandardButton combinations with or
* fix QAction.setShortcut() to accept string as argument
* fix QTreeWidgetItem comparison with <
* fix QTimer.timeout undeclared signal
* support all QSize and QSizeF operations
* improve signature of operations on QPolygon
* fix QLineEdit.setText() to accept None
* add QDialogButtonBox.StandardButton `__or__` operations
* fix missing methods being undetected for all Qt objects

See CHANGE_LOG.md for more details.

Please note that this work is far from complete. Don't hesitate to report problems or propose improvements.


# Licensing
As a derived work from PySide2, the stubs are delivered under the LGPL v2.1 . See file LICENSE for more details.


# Installation

Simply install PySide2-stubs with pip:

    $ pip install PySide2-stubs

Or clone the latest version from Github and install it via Python setuptools:

    $ git clone https://github.com/bluebird75/PySide2-stubs
    $ pip install .

That's it, the new stubs are picked up automatically by `mypy`. Typechecking process should be much better.


# Help improve the stubs

If you notice incorrect or missing typing information (mypy reports errors eventhough your code is correct), please report it
here with the following steps:

* create an issue showing your problem
* even better, create a PR to fix the problem
    * make sure to add a test showing what is mistyped. Just create a file under `tests/` , with a name
      not starting with *test*. The test suite will run the file and type-check it.
    * fix the stubs in the PySide2-stubs directory
    * and open the PR


