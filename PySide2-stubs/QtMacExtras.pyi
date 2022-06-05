# This Python file uses the following encoding: utf-8
#############################################################################
##
## Copyright (C) 2020 The Qt Company Ltd.
## Contact: https://www.qt.io/licensing/
##
## This file is part of Qt for Python.
##
## $QT_BEGIN_LICENSE:LGPL$
## Commercial License Usage
## Licensees holding valid commercial Qt licenses may use this file in
## accordance with the commercial license agreement provided with the
## Software or, alternatively, in accordance with the terms contained in
## a written agreement between you and The Qt Company. For licensing terms
## and conditions see https://www.qt.io/terms-conditions. For further
## information use the contact form at https://www.qt.io/contact-us.
##
## GNU Lesser General Public License Usage
## Alternatively, this file may be used under the terms of the GNU Lesser
## General Public License version 3 as published by the Free Software
## Foundation and appearing in the file LICENSE.LGPL3 included in the
## packaging of this file. Please review the following information to
## ensure the GNU Lesser General Public License version 3 requirements
## will be met: https://www.gnu.org/licenses/lgpl-3.0.html.
##
## GNU General Public License Usage
## Alternatively, this file may be used under the terms of the GNU
## General Public License version 2.0 or (at your option) the GNU General
## Public license version 3 or any later version approved by the KDE Free
## Qt Foundation. The licenses are as published by the Free Software
## Foundation and appearing in the file LICENSE.GPL2 and LICENSE.GPL3
## included in the packaging of this file. Please review the following
## information to ensure the GNU General Public License requirements will
## be met: https://www.gnu.org/licenses/gpl-2.0.html and
## https://www.gnu.org/licenses/gpl-3.0.html.
##
## $QT_END_LICENSE$
##
#############################################################################

"""
This file contains the exact signatures for all functions in module
PySide2.QtMacExtras, except for defaults which are replaced by "...".
"""

# Module PySide2.QtMacExtras
import PySide2
import typing

class Object(object): pass

import shiboken2 as Shiboken
Shiboken.Object = Object

import PySide2.QtCore
import PySide2.QtGui
import PySide2.QtMacExtras


class QMacPasteboardMime(Shiboken.Object):
    MIME_DND                 : QMacPasteboardMime.QMacPasteboardMimeType = ... # 0x1
    MIME_CLIP                : QMacPasteboardMime.QMacPasteboardMimeType = ... # 0x2
    MIME_ALL                 : QMacPasteboardMime.QMacPasteboardMimeType = ... # 0x3
    MIME_QT_CONVERTOR        : QMacPasteboardMime.QMacPasteboardMimeType = ... # 0x4
    MIME_QT3_CONVERTOR       : QMacPasteboardMime.QMacPasteboardMimeType = ... # 0x8

    class QMacPasteboardMimeType(object):
        MIME_DND                 : QMacPasteboardMime.QMacPasteboardMimeType = ... # 0x1
        MIME_CLIP                : QMacPasteboardMime.QMacPasteboardMimeType = ... # 0x2
        MIME_ALL                 : QMacPasteboardMime.QMacPasteboardMimeType = ... # 0x3
        MIME_QT_CONVERTOR        : QMacPasteboardMime.QMacPasteboardMimeType = ... # 0x4
        MIME_QT3_CONVERTOR       : QMacPasteboardMime.QMacPasteboardMimeType = ... # 0x8

    def __init__(self, arg__1:int) -> None: ...

    def canConvert(self, mime:str, flav:str) -> bool: ...
    def convertFromMime(self, mime:str, data:typing.Any, flav:str) -> typing.List: ...
    def convertToMime(self, mime:str, data:typing.Sequence, flav:str) -> typing.Any: ...
    def convertorName(self) -> str: ...
    def count(self, mimeData:PySide2.QtCore.QMimeData) -> int: ...
    def flavorFor(self, mime:str) -> str: ...
    def mimeFor(self, flav:str) -> str: ...


class QMacToolBar(PySide2.QtCore.QObject):

    @typing.overload
    def __init__(self, identifier:str, parent:typing.Optional[PySide2.QtCore.QObject]=...) -> None: ...
    @typing.overload
    def __init__(self, parent:typing.Optional[PySide2.QtCore.QObject]=...) -> None: ...

    def addAllowedItem(self, icon:PySide2.QtGui.QIcon, text:str) -> PySide2.QtMacExtras.QMacToolBarItem: ...
    def addAllowedStandardItem(self, standardItem:PySide2.QtMacExtras.QMacToolBarItem.StandardItem) -> PySide2.QtMacExtras.QMacToolBarItem: ...
    def addItem(self, icon:PySide2.QtGui.QIcon, text:str) -> PySide2.QtMacExtras.QMacToolBarItem: ...
    def addSeparator(self) -> None: ...
    def addStandardItem(self, standardItem:PySide2.QtMacExtras.QMacToolBarItem.StandardItem) -> PySide2.QtMacExtras.QMacToolBarItem: ...
    def allowedItems(self) -> typing.List: ...
    def attachToWindow(self, window:PySide2.QtGui.QWindow) -> None: ...
    def detachFromWindow(self) -> None: ...
    def items(self) -> typing.List: ...
    def setAllowedItems(self, allowedItems:typing.Sequence) -> None: ...
    def setItems(self, items:typing.Sequence) -> None: ...


class QMacToolBarItem(PySide2.QtCore.QObject):
    NoStandardItem           : QMacToolBarItem.StandardItem = ... # 0x0
    Space                    : QMacToolBarItem.StandardItem = ... # 0x1
    FlexibleSpace            : QMacToolBarItem.StandardItem = ... # 0x2

    class StandardItem(object):
        NoStandardItem           : QMacToolBarItem.StandardItem = ... # 0x0
        Space                    : QMacToolBarItem.StandardItem = ... # 0x1
        FlexibleSpace            : QMacToolBarItem.StandardItem = ... # 0x2

    def __init__(self, parent:typing.Optional[PySide2.QtCore.QObject]=...) -> None: ...

    def icon(self) -> PySide2.QtGui.QIcon: ...
    def selectable(self) -> bool: ...
    def setIcon(self, icon:PySide2.QtGui.QIcon) -> None: ...
    def setSelectable(self, selectable:bool) -> None: ...
    def setStandardItem(self, standardItem:PySide2.QtMacExtras.QMacToolBarItem.StandardItem) -> None: ...
    def setText(self, text:str) -> None: ...
    def standardItem(self) -> PySide2.QtMacExtras.QMacToolBarItem.StandardItem: ...
    def text(self) -> str: ...
@staticmethod
def qRegisterDraggedTypes(types:typing.Sequence) -> None: ...

# eof
