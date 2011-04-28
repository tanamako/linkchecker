# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010-2011 Bastian Kleineidam
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from PyQt4 import QtCore, QtGui

class LineEdit (QtGui.QLineEdit):
    """A line edit widget displaying a clear button if there is some text."""

    def __init__ (self, parent=None):
        """Initialize the clear button."""
        super(LineEdit, self).__init__(parent)
        self.clearButton = QtGui.QToolButton(self)
        pixmap = QtGui.QPixmap(":/icons/clear.png")
        self.clearButton.setIcon(QtGui.QIcon(pixmap))
        self.clearButton.setIconSize(pixmap.size())
        self.clearButton.setCursor(QtCore.Qt.ArrowCursor)
        style = "QToolButton { border: none; padding: 0px; }"
        self.clearButton.setStyleSheet(style)
        self.clearButton.hide()
        self.clearButton.clicked.connect(self.clear)
        self.textChanged.connect(self.updateCloseButton)
        frameWidth = self.style().pixelMetric(QtGui.QStyle.PM_DefaultFrameWidth)
        padding = self.clearButton.sizeHint().width() + frameWidth + 1
        self.setStyleSheet("QLineEdit { padding-right: %dpx; } " % padding)
        mSize = self.minimumSizeHint()
        sizeHint = self.clearButton.sizeHint()
        mWidth = max(mSize.width(), sizeHint.width() + frameWidth * 2 + 2)
        mHeight = max(mSize.height(), sizeHint.height() + frameWidth * 2 + 2)
        self.setMinimumSize(mWidth, mHeight)

    def resizeEvent (self, event):
        """Move the clear button due to resize event."""
        sizeHint = self.clearButton.sizeHint()
        frameWidth = self.style().pixelMetric(QtGui.QStyle.PM_DefaultFrameWidth)
        x = self.rect().right() - frameWidth - sizeHint.width()
        y = (self.rect().bottom() + 1 - sizeHint.height())/2
        self.clearButton.move(x,y)

    def updateCloseButton (self, text):
        """Only display the clear button if there is some text."""
        self.clearButton.setVisible(bool(text))

    def contextMenuEvent (self, event):
        """Add Firefox bookmark action to context menu."""
        menu = self.createStandardContextMenu()
        if find_firefox():
            action = menu.addAction(_("Insert Firefox bookmark file"))
            action.triggered.connect(lambda: self.setText(find_firefox()))
        if find_chromium():
            action = menu.addAction(_("Insert Google Chrome bookmark file"))
            action.triggered.connect(lambda: self.setText(find_chromium()))
        if find_opera():
            action = menu.addAction(_("Insert Opera bookmark file"))
            action.triggered.connect(lambda: self.setText(find_opera()))
        menu.exec_(event.globalPos())


def find_firefox ():
    """Return Firefox bookmark filename or empty string if not found."""
    from ..bookmarks.firefox import find_bookmark_file
    return find_bookmark_file()


def find_chromium ():
    """Return Google Chrome bookmark filename or empty string if not found."""
    from ..bookmarks.chromium import find_bookmark_file
    return find_bookmark_file()


def find_opera ():
    """Return Opera bookmark filename or empty string if not found."""
    from ..bookmarks.opera import find_bookmark_file
    return find_bookmark_file()
