


Version 5.15.2.1.0:
===================
Initial release for PySide2 v5.15.2.1

* fix Signal to make it accept method emit()
* fix qVersion() returns string, not bytes
* fix QMessageBox.warning, information, critical, question, about, aboutQt to accept None as parent argument
* fix QProgressDialog.setCancelButton() accepting None
* fix QTreeWidget.topLevelItem() returning possibly None
* fix QMessageBox.StandardButton or combinations
* fix QProcess.ExitStatus enum conversion to int
* fix QAction.setShortcut() to accept string as argument
* fix QTreeWidgetItem comparison with < 
* fix Signal.connect() return value to bool instead of None
* fix QTimer.timeout undeclared signal
* support all QSize and QSizeF operations
* improve signature of operations on QPolygon
* improve QPainter methods which use lists of QPoint in entry
* improve QObject.findChildren() type information
* fix QLineEdit.setText() to accept None
* add QDialogButtonBox.StandardButton __or__ operations
* fix Slot() argument and return value type-checking
* fix missing methods being undetected for all Qt objects
* add platform-specific stubs: QMacExtras, QWinExtras, QX11Extras
