import sys
from typing import Optional

from PySide6.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem,  QFileDialog
from PySide6.QtCore import Qt
from PySide6.QtGui import QShortcut, QKeySequence
from pikepdf import OutlineItem, Dictionary

from mainwindow_ui import Ui_MainWindow
from PdfOutlineParser import PdfOutlineParser


class MainWindow(QMainWindow):
    class ShortCut:
        rename: QShortcut
        move_left: QShortcut
        move_right: QShortcut
        move_up: QShortcut
        move_down: QShortcut
        delete: QShortcut
        save: QShortcut

        def setEnable(self, enable: bool):
            for shortcut in [self.rename,
                             self.move_left,
                             self.move_right,
                             self.move_up,
                             self.move_down,
                             self.delete,
                             self.save]:
                shortcut.setEnabled(enable)

    """
    Handler for QTreeWidget and QTreeWidgetItem, 
    combine their common functions
    """
    class TreeHandler:
        def __init__(self, treeWidget: QTreeWidget):
            self.root = treeWidget

        def takeChild(self, parent: Optional[QTreeWidgetItem], index: int):
            if parent is None:
                return self.root.takeTopLevelItem(index)
            else:
                return parent.takeChild(index)

        def indexOfChild(self, parent: Optional[QTreeWidgetItem], child: QTreeWidgetItem):
            if parent is None:
                return self.root.indexOfTopLevelItem(child)
            else:
                return parent.indexOfChild(child)

        def insertChild(self, parent: Optional[QTreeWidgetItem],
                        index: int, child: QTreeWidgetItem):
            if parent is None:
                return self.root.insertTopLevelItem(index, child)
            else:
                return parent.insertChild(index, child)

        def addChild(self, parent: Optional[QTreeWidgetItem], child: QTreeWidgetItem):
            if parent is None:
                return self.root.addTopLevelItem(child)
            else:
                return parent.addChild(child)

        def childCount(self, parent: Optional[QTreeWidgetItem]):
            if parent is None:
                return self.root.topLevelItemCount()
            else:
                return parent.childCount()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.shortcutInit()
        self.eventInit()

        self.mapping: dict[QTreeWidgetItem, OutlineItem] = {}

        self.parser = PdfOutlineParser()

        self.tree = MainWindow.TreeHandler(self.ui.outline)

    def shortcutInit(self):
        self.shortcut = MainWindow.ShortCut()
        shortcut = self.shortcut
        shortcut.rename = QShortcut(QKeySequence(Qt.Key.Key_F2), self)
        shortcut.rename.activated.connect(self.editShortcutClicked)
        shortcut.move_left = QShortcut(QKeySequence(Qt.Key.Key_Left), self)
        shortcut.move_left.activated.connect(self.moveOut)
        shortcut.move_right = QShortcut(QKeySequence(Qt.Key.Key_Right), self)
        shortcut.move_right.activated.connect(self.moveIn)
        shortcut.move_up = QShortcut(QKeySequence(Qt.Key.Key_Up), self)
        shortcut.move_up.activated.connect(self.selectPrev)
        shortcut.move_down = QShortcut(QKeySequence(Qt.Key.Key_Down), self)
        shortcut.move_down.activated.connect(self.selectNext)
        shortcut.delete = QShortcut(QKeySequence(Qt.Key.Key_Delete), self)
        shortcut.delete.activated.connect(self.deleteSelectedItem)
        shortcut.save = QShortcut(QKeySequence("Ctrl+S"), self)
        shortcut.save.activated.connect(self.save)
        shortcut.setEnable(False)

    def eventInit(self):
        self.ui.open_file.clicked.connect(self.loadFile)
        self.ui.remove.clicked.connect(self.deleteSelectedItem)
        self.ui.add_before.clicked.connect(self.addItemBefore)
        self.ui.add_after.clicked.connect(self.addItemAfter)
        self.ui.move_right.clicked.connect(self.moveIn)
        self.ui.move_left.clicked.connect(self.moveOut)
        self.ui.move_up.clicked.connect(self.moveUp)
        self.ui.move_down.clicked.connect(self.moveDown)
        self.ui.save.clicked.connect(self.save)
        self.ui.outline.itemChanged.connect(self.contentEdited)
        self.ui.remove_all.clicked.connect(self.clearAll)

    def loadFile(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, caption="Open file", dir="./", filter="pdf file(*.pdf)")
        if len(filename) == 0:
            return

        self.ui.filename.setText(filename)
        self.parser.open(filename)

        def build_outline(parent_widget: Optional[QTreeWidgetItem], children: list[OutlineItem]):
            for child in children:
                name = child.title
                if child.destination is None:
                    if child.action is None:
                        target = "None"
                    else:
                        target = f"{child.action.D},{child.action.S}"
                else:
                    for i, p in enumerate(self.parser.pdf.pages):
                        if child.destination[0] == p.obj:
                            target = f"{i}"
                            break

                item = self.addItem(name, target)
                self.mapping[item] = child

                self.tree.addChild(parent_widget, item)
                build_outline(item, child.children)
        build_outline(None, self.parser.outline.root)

        self.ui.outline.expandAll()

        self.ui.move_down.setEnabled(True)
        self.ui.move_up.setEnabled(True)
        self.ui.move_left.setEnabled(True)
        self.ui.move_right.setEnabled(True)
        self.ui.add_after.setEnabled(True)
        self.ui.add_before.setEnabled(True)
        self.ui.remove.setEnabled(True)
        self.ui.remove_all.setEnabled(True)
        self.ui.save.setEnabled(True)
        self.shortcut.setEnable(True)
        self.ui.page_mode.setEnabled(True)

    def addItem(self, name: str, target: str):
        item = QTreeWidgetItem()
        item.setText(0, name)
        item.setText(1, target)
        item.setExpanded(True)
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
        return item

    def addItemOffset(self, name: str, page: int, offset: int):
        name = 'new item'
        page = 0

        new_item = self.addItem(name, str(page))

        # nothing in outline, insert at top
        if self.ui.outline.topLevelItemCount() == 0:
            self.ui.outline.insertTopLevelItem(0, new_item)
            new_child = self.parser.add_child_offset(name, page, None, None)
            self.mapping[new_item] = new_child

            self.ui.outline.setCurrentItem(new_item)
            return

        item = self.ui.outline.currentItem()
        if item is None:
            return

        parent = item.parent()
        index = self.tree.indexOfChild(parent, item)+offset
        self.tree.insertChild(parent, index, new_item)
        new_child = self.parser.add_child_offset(name, page,
                                                 self.mapping.get(parent, None), self.mapping[item], offset)

        self.mapping[new_item] = new_child

    def addItemAfter(self):
        name = 'new item'
        page = 0

        self.addItemOffset(name, page, 1)

    def addItemBefore(self):
        name = 'new item'
        page = 0

        self.addItemOffset(name, page, 0)

    def moveIn(self):
        item = self.ui.outline.currentItem()
        if item is None:
            return

        prev_item = self.ui.outline.itemAbove(item)
        if prev_item is None:
            return

        # same level
        parent = item.parent()
        if prev_item == parent:  # already parent, forbid
            return

        # remove from old parent
        index = self.tree.indexOfChild(parent, item)
        self.tree.takeChild(parent, index)

        # prev item may nest deeper, try to find same parent
        while prev_item.parent() != parent:
            prev_item = prev_item.parent()
        prev_item.addChild(item)

        self.ui.outline.setCurrentItem(item)

        self.parser.moveIn(self.mapping[item])

    def moveUp(self):
        item = self.ui.outline.currentItem()
        if item is None:
            return

        parent = item.parent()

        index = self.tree.indexOfChild(parent, item)
        if index == 0:
            return
        self.tree.takeChild(parent, index)
        self.tree.insertChild(parent, index - 1, item)

        self.ui.outline.setCurrentItem(item)

        self.parser.moveUp(self.mapping[item])

    def moveDown(self):
        item = self.ui.outline.currentItem()
        if item is None:
            return

        parent = item.parent()
        # remove from old parent
        index = self.tree.indexOfChild(parent, item)
        if index == self.tree.childCount(parent) - 1:
            return
        self.tree.takeChild(parent, index)
        self.tree.insertChild(parent, index + 1, item)

        self.ui.outline.setCurrentItem(item)

        self.parser.moveDown(self.mapping[item])

    def moveOut(self):
        item = self.ui.outline.currentItem()
        if item is None:
            return

        # already root
        parent = item.parent()
        if parent is None:
            return

        grandparent = parent.parent()

        # remove from original parent
        index = self.tree.indexOfChild(parent, item)
        self.tree.takeChild(parent, index)

        # original parent become prev sibling
        prev_index = self.tree.indexOfChild(grandparent, parent)
        self.tree.insertChild(grandparent, prev_index+1, item)

        self.ui.outline.setCurrentItem(item)

        self.parser.moveOut(self.mapping[item])

    def deleteSelectedItem(self):
        item = self.ui.outline.currentItem()
        if item is None:
            return

        element = self.mapping[item]
        self.parser.removeChild(element)
        del self.mapping[item]

        if item.parent() is None:
            index = self.ui.outline.currentIndex()
            self.ui.outline.takeTopLevelItem(index.row())
        else:
            item.parent().removeChild(item)
        # self.ui.outline.removeItemWidget(item, index.column())

    def clearAll(self):
        self.ui.outline.clear()
        self.mapping.clear()
        self.parser.clear()

    def contentEdited(self, item: QTreeWidgetItem, column: int):
        if column == 0:
            self.parser.edit_node_name(self.mapping[item], item.text(0))
        elif column == 1:
            self.parser.edit_node_target_page(self.mapping[item],
                                              int(item.text(1))-1)

    def editShortcutClicked(self):
        item = self.ui.outline.currentItem()
        column = self.ui.outline.currentColumn()
        if item is not None:
            self.ui.outline.editItem(item, column)

    def selectPrev(self):
        item = self.ui.outline.currentItem()
        if item is None:
            return
        prev_item = self.ui.outline.itemAbove(item)
        if prev_item is not None:
            self.ui.outline.setCurrentItem(prev_item)

    def selectNext(self):
        item = self.ui.outline.currentItem()
        if item is None:
            return
        next_item = self.ui.outline.itemBelow(item)
        if next_item is not None:
            self.ui.outline.setCurrentItem(next_item)

    def save(self):
        filename, _ = QFileDialog.getSaveFileName(self, 'Save File',
                                                  f'./', 'pdf (*.pdf)')
        if len(filename) == 0:
            return

        if self.ui.page_mode_none.isChecked():
            page_mode = "UseNone"
        elif self.ui.page_mode_outlines.isChecked():
            page_mode = "UseOutlines"
        elif self.ui.page_mode_thumbs.isChecked():
            page_mode = "UseThumbs"
        elif self.ui.page_mode_fullscreen.isChecked():
            page_mode = "FullScreen"
        elif self.ui.page_mode_oc.isChecked():
            page_mode = "UseOC"
        elif self.ui.page_mode_attachments.isChecked():
            page_mode = "UseAttachment"
        self.parser.save(filename, page_mode)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
