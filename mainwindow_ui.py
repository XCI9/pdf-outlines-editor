# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGroupBox, QHeaderView, QLabel,
    QLineEdit, QMainWindow, QPushButton, QRadioButton,
    QSizePolicy, QToolButton, QTreeWidget, QTreeWidgetItem,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(495, 493)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 50, 53, 16))
        self.add_before = QPushButton(self.centralwidget)
        self.add_before.setObjectName(u"add_before")
        self.add_before.setEnabled(False)
        self.add_before.setGeometry(QRect(390, 130, 75, 24))
        self.outline = QTreeWidget(self.centralwidget)
        self.outline.setObjectName(u"outline")
        self.outline.setGeometry(QRect(20, 70, 351, 411))
        self.remove = QPushButton(self.centralwidget)
        self.remove.setObjectName(u"remove")
        self.remove.setEnabled(False)
        self.remove.setGeometry(QRect(390, 100, 75, 24))
        self.move_right = QPushButton(self.centralwidget)
        self.move_right.setObjectName(u"move_right")
        self.move_right.setEnabled(False)
        self.move_right.setGeometry(QRect(445, 205, 21, 21))
        self.move_left = QPushButton(self.centralwidget)
        self.move_left.setObjectName(u"move_left")
        self.move_left.setEnabled(False)
        self.move_left.setGeometry(QRect(395, 205, 21, 21))
        self.save = QPushButton(self.centralwidget)
        self.save.setObjectName(u"save")
        self.save.setEnabled(False)
        self.save.setGeometry(QRect(390, 450, 75, 24))
        self.filename = QLineEdit(self.centralwidget)
        self.filename.setObjectName(u"filename")
        self.filename.setGeometry(QRect(20, 10, 421, 21))
        self.open_file = QToolButton(self.centralwidget)
        self.open_file.setObjectName(u"open_file")
        self.open_file.setGeometry(QRect(420, 11, 18, 18))
        self.remove_all = QPushButton(self.centralwidget)
        self.remove_all.setObjectName(u"remove_all")
        self.remove_all.setEnabled(False)
        self.remove_all.setGeometry(QRect(390, 70, 75, 24))
        self.move_up = QPushButton(self.centralwidget)
        self.move_up.setObjectName(u"move_up")
        self.move_up.setEnabled(False)
        self.move_up.setGeometry(QRect(420, 190, 21, 21))
        self.move_down = QPushButton(self.centralwidget)
        self.move_down.setObjectName(u"move_down")
        self.move_down.setEnabled(False)
        self.move_down.setGeometry(QRect(420, 220, 21, 21))
        self.add_after = QPushButton(self.centralwidget)
        self.add_after.setObjectName(u"add_after")
        self.add_after.setEnabled(False)
        self.add_after.setGeometry(QRect(390, 160, 75, 24))
        self.page_mode = QGroupBox(self.centralwidget)
        self.page_mode.setObjectName(u"page_mode")
        self.page_mode.setEnabled(False)
        self.page_mode.setGeometry(QRect(390, 299, 91, 141))
        self.page_mode_none = QRadioButton(self.page_mode)
        self.page_mode_none.setObjectName(u"page_mode_none")
        self.page_mode_none.setGeometry(QRect(10, 20, 71, 20))
        self.page_mode_none.setChecked(True)
        self.page_mode_outlines = QRadioButton(self.page_mode)
        self.page_mode_outlines.setObjectName(u"page_mode_outlines")
        self.page_mode_outlines.setGeometry(QRect(10, 40, 71, 20))
        self.page_mode_thumbs = QRadioButton(self.page_mode)
        self.page_mode_thumbs.setObjectName(u"page_mode_thumbs")
        self.page_mode_thumbs.setGeometry(QRect(10, 60, 71, 20))
        self.page_mode_fullscreen = QRadioButton(self.page_mode)
        self.page_mode_fullscreen.setObjectName(u"page_mode_fullscreen")
        self.page_mode_fullscreen.setGeometry(QRect(10, 80, 71, 20))
        self.page_mode_oc = QRadioButton(self.page_mode)
        self.page_mode_oc.setObjectName(u"page_mode_oc")
        self.page_mode_oc.setGeometry(QRect(10, 100, 71, 20))
        self.page_mode_attachments = QRadioButton(self.page_mode)
        self.page_mode_attachments.setObjectName(u"page_mode_attachments")
        self.page_mode_attachments.setGeometry(QRect(10, 120, 71, 20))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u76ee\u9304", None))
        self.add_before.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u589e\u65bc\u4e0a", None))
        ___qtreewidgetitem = self.outline.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("MainWindow", u"\u76ee\u6a19\u9801\u6578", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"\u76ee\u9304", None));
        self.remove.setText(QCoreApplication.translate("MainWindow", u"\u522a\u9664", None))
        self.move_right.setText(QCoreApplication.translate("MainWindow", u">", None))
        self.move_left.setText(QCoreApplication.translate("MainWindow", u"<", None))
        self.save.setText(QCoreApplication.translate("MainWindow", u"\u5b58\u6a94", None))
        self.open_file.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.remove_all.setText(QCoreApplication.translate("MainWindow", u"\u5168\u90e8\u6e05\u9664", None))
        self.move_up.setText(QCoreApplication.translate("MainWindow", u"^", None))
        self.move_down.setText(QCoreApplication.translate("MainWindow", u"v", None))
        self.add_after.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u589e\u65bc\u4e0b", None))
        self.page_mode.setTitle(QCoreApplication.translate("MainWindow", u"\u986f\u793a\u6a21\u5f0f", None))
        self.page_mode_none.setText(QCoreApplication.translate("MainWindow", u"\u7121", None))
        self.page_mode_outlines.setText(QCoreApplication.translate("MainWindow", u"\u986f\u793a\u76ee\u9304", None))
        self.page_mode_thumbs.setText(QCoreApplication.translate("MainWindow", u"\u986f\u793a\u7e2e\u5716", None))
        self.page_mode_fullscreen.setText(QCoreApplication.translate("MainWindow", u"\u5168\u87a2\u5e55", None))
        self.page_mode_oc.setText(QCoreApplication.translate("MainWindow", u"\u986f\u793a\u5716\u5c64", None))
        self.page_mode_attachments.setText(QCoreApplication.translate("MainWindow", u"\u986f\u793a\u9644\u4ef6", None))
    # retranslateUi

