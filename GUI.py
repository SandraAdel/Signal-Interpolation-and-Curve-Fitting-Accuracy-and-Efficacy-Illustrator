# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\spring22\SBEN311\TASKSS\task#4\Interpolation-Curve-Fitting-App\GUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1382, 810)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.mainGraphAndErrorMapGridLayout = QtWidgets.QGridLayout()
        self.mainGraphAndErrorMapGridLayout.setObjectName("mainGraphAndErrorMapGridLayout")
        self.mainGraphGraphicsView = PlotWidget(self.centralwidget)
        self.mainGraphGraphicsView.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.mainGraphGraphicsView.setObjectName("mainGraphGraphicsView")
        self.mainGraphAndErrorMapGridLayout.addWidget(self.mainGraphGraphicsView, 1, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(850, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.mainGraphAndErrorMapGridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.latexEquationLabel = QtWidgets.QLabel(self.centralwidget)
        self.latexEquationLabel.setObjectName("latexEquationLabel")
        self.mainGraphAndErrorMapGridLayout.addWidget(self.latexEquationLabel, 0, 0, 1, 1)
        self.errorMapGraphicsView = PlotWidget(self.centralwidget)
        self.errorMapGraphicsView.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.errorMapGraphicsView.setObjectName("errorMapGraphicsView")
        self.mainGraphAndErrorMapGridLayout.addWidget(self.errorMapGraphicsView, 1, 1, 1, 1)
        self.errorLabel = QtWidgets.QLabel(self.centralwidget)
        self.errorLabel.setObjectName("errorLabel")
        self.mainGraphAndErrorMapGridLayout.addWidget(self.errorLabel, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.mainGraphAndErrorMapGridLayout)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        spacerItem1 = QtWidgets.QSpacerItem(20, 320, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem1, 0, 1, 1, 1)
        self.errorMapControlsGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.errorMapControlsGroupBox.setObjectName("errorMapControlsGroupBox")
        self.generateAndCancelErrorMapPushButton = QtWidgets.QPushButton(self.errorMapControlsGroupBox)
        self.generateAndCancelErrorMapPushButton.setGeometry(QtCore.QRect(190, 110, 271, 31))
        self.generateAndCancelErrorMapPushButton.setObjectName("generateAndCancelErrorMapPushButton")
        self.errorMapProgressBar = QtWidgets.QProgressBar(self.errorMapControlsGroupBox)
        self.errorMapProgressBar.setGeometry(QtCore.QRect(10, 160, 601, 24))
        self.errorMapProgressBar.setProperty("value", 24)
        self.errorMapProgressBar.setObjectName("errorMapProgressBar")
        self.layoutWidget = QtWidgets.QWidget(self.errorMapControlsGroupBox)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 20, 641, 99))
        self.layoutWidget.setObjectName("layoutWidget")
        self.xAxisAndYAxisGridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.xAxisAndYAxisGridLayout.setContentsMargins(0, 0, 0, 0)
        self.xAxisAndYAxisGridLayout.setObjectName("xAxisAndYAxisGridLayout")
        self.xAxisLabel = QtWidgets.QLabel(self.layoutWidget)
        self.xAxisLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.xAxisLabel.setObjectName("xAxisLabel")
        self.xAxisAndYAxisGridLayout.addWidget(self.xAxisLabel, 0, 0, 1, 1)
        self.xAxisComboBox = QtWidgets.QComboBox(self.layoutWidget)
        self.xAxisComboBox.setObjectName("xAxisComboBox")
        self.xAxisComboBox.addItem("")
        self.xAxisComboBox.addItem("")
        self.xAxisComboBox.addItem("")
        self.xAxisAndYAxisGridLayout.addWidget(self.xAxisComboBox, 0, 2, 1, 1)
        self.yAxisLabel = QtWidgets.QLabel(self.layoutWidget)
        self.yAxisLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.yAxisLabel.setObjectName("yAxisLabel")
        self.xAxisAndYAxisGridLayout.addWidget(self.yAxisLabel, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.xAxisAndYAxisGridLayout.addWidget(self.label, 2, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(120, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.xAxisAndYAxisGridLayout.addItem(spacerItem2, 0, 3, 1, 1)
        self.yAxisComboBox = QtWidgets.QComboBox(self.layoutWidget)
        self.yAxisComboBox.setObjectName("yAxisComboBox")
        self.yAxisComboBox.addItem("")
        self.yAxisComboBox.addItem("")
        self.yAxisComboBox.addItem("")
        self.xAxisAndYAxisGridLayout.addWidget(self.yAxisComboBox, 1, 2, 1, 1)
        self.gridLayout.addWidget(self.errorMapControlsGroupBox, 0, 2, 1, 1)
        self.mainGraphControlsGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.mainGraphControlsGroupBox.setObjectName("mainGraphControlsGroupBox")
        self.layoutWidget1 = QtWidgets.QWidget(self.mainGraphControlsGroupBox)
        self.layoutWidget1.setGeometry(QtCore.QRect(41, 36, 561, 271))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.mainGraphControlsGridLayout = QtWidgets.QGridLayout(self.layoutWidget1)
        self.mainGraphControlsGridLayout.setContentsMargins(0, 0, 0, 0)
        self.mainGraphControlsGridLayout.setObjectName("mainGraphControlsGridLayout")
        self.bicubicRadioButton = QtWidgets.QRadioButton(self.layoutWidget1)
        self.bicubicRadioButton.setObjectName("bicubicRadioButton")
        self.mainGraphControlsGridLayout.addWidget(self.bicubicRadioButton, 0, 0, 1, 1)
        self.cubicSplineRadioButton = QtWidgets.QRadioButton(self.layoutWidget1)
        self.cubicSplineRadioButton.setObjectName("cubicSplineRadioButton")
        self.mainGraphControlsGridLayout.addWidget(self.cubicSplineRadioButton, 0, 1, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.mainGraphControlsGridLayout.addItem(spacerItem3, 0, 2, 1, 1)
        self.polynomialRadioButton = QtWidgets.QRadioButton(self.layoutWidget1)
        self.polynomialRadioButton.setObjectName("polynomialRadioButton")
        self.mainGraphControlsGridLayout.addWidget(self.polynomialRadioButton, 0, 3, 1, 1)
        self.cubicSplineFittingOrderLabel = QtWidgets.QLabel(self.layoutWidget1)
        self.cubicSplineFittingOrderLabel.setObjectName("cubicSplineFittingOrderLabel")
        self.mainGraphControlsGridLayout.addWidget(self.cubicSplineFittingOrderLabel, 1, 1, 1, 1)
        self.polynomialFittingOrderSpinBox = QtWidgets.QSpinBox(self.layoutWidget1)
        self.polynomialFittingOrderSpinBox.setObjectName("polynomialFittingOrderSpinBox")
        self.mainGraphControlsGridLayout.addWidget(self.polynomialFittingOrderSpinBox, 2, 3, 1, 1)
        self.polynomialMultipleChunksRadioButton = QtWidgets.QRadioButton(self.layoutWidget1)
        self.polynomialMultipleChunksRadioButton.setObjectName("polynomialMultipleChunksRadioButton")
        self.mainGraphControlsGridLayout.addWidget(self.polynomialMultipleChunksRadioButton, 4, 3, 1, 1)
        self.polynomialFittingOrderLabel = QtWidgets.QLabel(self.layoutWidget1)
        self.polynomialFittingOrderLabel.setObjectName("polynomialFittingOrderLabel")
        self.mainGraphControlsGridLayout.addWidget(self.polynomialFittingOrderLabel, 1, 3, 1, 1)
        self.polynomialNumberOfChunksSpinBox = QtWidgets.QSpinBox(self.layoutWidget1)
        self.polynomialNumberOfChunksSpinBox.setObjectName("polynomialNumberOfChunksSpinBox")
        self.mainGraphControlsGridLayout.addWidget(self.polynomialNumberOfChunksSpinBox, 6, 3, 1, 1)
        self.polynomialOerlapSpinBox = QtWidgets.QSpinBox(self.layoutWidget1)
        self.polynomialOerlapSpinBox.setObjectName("polynomialOerlapSpinBox")
        self.mainGraphControlsGridLayout.addWidget(self.polynomialOerlapSpinBox, 10, 3, 1, 1)
        self.polynomialNumberOfChunksLabel = QtWidgets.QLabel(self.layoutWidget1)
        self.polynomialNumberOfChunksLabel.setObjectName("polynomialNumberOfChunksLabel")
        self.mainGraphControlsGridLayout.addWidget(self.polynomialNumberOfChunksLabel, 5, 3, 1, 1)
        self.polynomialOverlapLabel = QtWidgets.QLabel(self.layoutWidget1)
        self.polynomialOverlapLabel.setObjectName("polynomialOverlapLabel")
        self.mainGraphControlsGridLayout.addWidget(self.polynomialOverlapLabel, 9, 3, 1, 1)
        self.polynomialFitPushButton = QtWidgets.QPushButton(self.layoutWidget1)
        self.polynomialFitPushButton.setObjectName("polynomialFitPushButton")
        self.mainGraphControlsGridLayout.addWidget(self.polynomialFitPushButton, 11, 3, 1, 1)
        self.polynomialOneChunkRadioButton = QtWidgets.QRadioButton(self.layoutWidget1)
        self.polynomialOneChunkRadioButton.setObjectName("polynomialOneChunkRadioButton")
        self.mainGraphControlsGridLayout.addWidget(self.polynomialOneChunkRadioButton, 3, 3, 1, 1)
        self.cubicSplineFittingOrderSpinBox = QtWidgets.QSpinBox(self.layoutWidget1)
        self.cubicSplineFittingOrderSpinBox.setObjectName("cubicSplineFittingOrderSpinBox")
        self.mainGraphControlsGridLayout.addWidget(self.cubicSplineFittingOrderSpinBox, 2, 1, 1, 1)
        self.gridLayout.addWidget(self.mainGraphControlsGroupBox, 0, 0, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem4, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1382, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.openAction = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.openAction.setIcon(icon)
        self.openAction.setObjectName("openAction")
        self.menuFile.addAction(self.openAction)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.latexEquationLabel.setText(_translate("MainWindow", "Latex equation"))
        self.errorLabel.setText(_translate("MainWindow", "Error map"))
        self.errorMapControlsGroupBox.setTitle(_translate("MainWindow", "Error map controls"))
        self.generateAndCancelErrorMapPushButton.setText(_translate("MainWindow", "Generate error map"))
        self.xAxisLabel.setText(_translate("MainWindow", "X-axis"))
        self.xAxisComboBox.setItemText(0, _translate("MainWindow", "Order of polynomial"))
        self.xAxisComboBox.setItemText(1, _translate("MainWindow", "Number of chunks"))
        self.xAxisComboBox.setItemText(2, _translate("MainWindow", "Overlapping"))
        self.yAxisLabel.setText(_translate("MainWindow", "Y-axis"))
        self.label.setText(_translate("MainWindow", "ZO3BAAAR"))
        self.yAxisComboBox.setItemText(0, _translate("MainWindow", "Order of polynomial"))
        self.yAxisComboBox.setItemText(1, _translate("MainWindow", "Number of chunks"))
        self.yAxisComboBox.setItemText(2, _translate("MainWindow", "Overlapping"))
        self.mainGraphControlsGroupBox.setTitle(_translate("MainWindow", "Main Graph Controls"))
        self.bicubicRadioButton.setText(_translate("MainWindow", "Bicubic"))
        self.cubicSplineRadioButton.setText(_translate("MainWindow", "Cubic Spline"))
        self.polynomialRadioButton.setText(_translate("MainWindow", "Polynomial"))
        self.cubicSplineFittingOrderLabel.setText(_translate("MainWindow", "Fitting order"))
        self.polynomialMultipleChunksRadioButton.setText(_translate("MainWindow", "Multiple Chunks"))
        self.polynomialFittingOrderLabel.setText(_translate("MainWindow", "Fitting order"))
        self.polynomialNumberOfChunksLabel.setText(_translate("MainWindow", "Number of chunks"))
        self.polynomialOverlapLabel.setText(_translate("MainWindow", "overlap"))
        self.polynomialFitPushButton.setText(_translate("MainWindow", "Fit"))
        self.polynomialOneChunkRadioButton.setText(_translate("MainWindow", "One Chunk"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.openAction.setText(_translate("MainWindow", "Open"))
        self.openAction.setShortcut(_translate("MainWindow", "Ctrl+O"))
from pyqtgraph import PlotWidget



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
