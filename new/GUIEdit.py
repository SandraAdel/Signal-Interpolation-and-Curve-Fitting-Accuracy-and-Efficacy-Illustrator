# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\spring22\SBEN311\TASKSS\task#4\edit\GUI2.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1322, 925)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.latexEquationComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.latexEquationComboBox.setObjectName("latexEquationComboBox")
        self.gridLayout_4.addWidget(self.latexEquationComboBox, 0, 1, 1, 1)
        self.latexEquationLabel = QtWidgets.QLabel(self.centralwidget)
        self.latexEquationLabel.setText("")
        self.latexEquationLabel.setObjectName("latexEquationLabel")
        self.gridLayout_4.addWidget(self.latexEquationLabel, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_4)
        self.mainGraphAndErrorMapGridLayout = QtWidgets.QGridLayout()
        self.mainGraphAndErrorMapGridLayout.setObjectName("mainGraphAndErrorMapGridLayout")
        self.mainGraphGraphicsView = PlotWidget(self.centralwidget)
        self.mainGraphGraphicsView.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.mainGraphGraphicsView.setObjectName("mainGraphGraphicsView")
        self.mainGraphAndErrorMapGridLayout.addWidget(self.mainGraphGraphicsView, 0, 0, 1, 1)
        self.errorMapGridLayout = QtWidgets.QGridLayout()
        self.errorMapGridLayout.setObjectName("errorMapGridLayout")
        self.errorMapGraphicsView = PlotWidget(self.centralwidget)
        self.errorMapGraphicsView.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.errorMapGraphicsView.setObjectName("errorMapGraphicsView")
        self.errorMapGridLayout.addWidget(self.errorMapGraphicsView, 0, 0, 1, 1)
        self.mainGraphAndErrorMapGridLayout.addLayout(self.errorMapGridLayout, 0, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(13, 300, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.mainGraphAndErrorMapGridLayout.addItem(spacerItem, 0, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(700, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.mainGraphAndErrorMapGridLayout.addItem(spacerItem1, 1, 0, 1, 1)
        self.verticalLayout.addLayout(self.mainGraphAndErrorMapGridLayout)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.errorMapControlsGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(100)
        sizePolicy.setHeightForWidth(self.errorMapControlsGroupBox.sizePolicy().hasHeightForWidth())
        self.errorMapControlsGroupBox.setSizePolicy(sizePolicy)
        self.errorMapControlsGroupBox.setObjectName("errorMapControlsGroupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.errorMapControlsGroupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.xAxisAndYAxisGridLayout = QtWidgets.QGridLayout()
        self.xAxisAndYAxisGridLayout.setObjectName("xAxisAndYAxisGridLayout")
        spacerItem2 = QtWidgets.QSpacerItem(120, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.xAxisAndYAxisGridLayout.addItem(spacerItem2, 0, 4, 1, 1)
        self.xAxisComboBox = QtWidgets.QComboBox(self.errorMapControlsGroupBox)
        self.xAxisComboBox.setObjectName("xAxisComboBox")
        self.xAxisComboBox.addItem("")
        self.xAxisComboBox.addItem("")
        self.xAxisComboBox.addItem("")
        self.xAxisComboBox.addItem("")
        self.xAxisAndYAxisGridLayout.addWidget(self.xAxisComboBox, 0, 3, 1, 1)
        self.startAndCancelErrorMapPushButton = QtWidgets.QPushButton(self.errorMapControlsGroupBox)
        self.startAndCancelErrorMapPushButton.setObjectName("startAndCancelErrorMapPushButton")
        self.xAxisAndYAxisGridLayout.addWidget(self.startAndCancelErrorMapPushButton, 3, 1, 1, 1)
        self.xAxisLabel = QtWidgets.QLabel(self.errorMapControlsGroupBox)
        self.xAxisLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.xAxisLabel.setObjectName("xAxisLabel")
        self.xAxisAndYAxisGridLayout.addWidget(self.xAxisLabel, 0, 1, 1, 1)
        self.yAxisComboBox = QtWidgets.QComboBox(self.errorMapControlsGroupBox)
        self.yAxisComboBox.setObjectName("yAxisComboBox")
        self.yAxisComboBox.addItem("")
        self.yAxisComboBox.addItem("")
        self.yAxisComboBox.addItem("")
        self.yAxisComboBox.addItem("")
        self.xAxisAndYAxisGridLayout.addWidget(self.yAxisComboBox, 1, 3, 1, 1)
        self.label = QtWidgets.QLabel(self.errorMapControlsGroupBox)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.xAxisAndYAxisGridLayout.addWidget(self.label, 2, 1, 1, 1)
        self.yAxisLabel = QtWidgets.QLabel(self.errorMapControlsGroupBox)
        self.yAxisLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.yAxisLabel.setObjectName("yAxisLabel")
        self.xAxisAndYAxisGridLayout.addWidget(self.yAxisLabel, 1, 1, 1, 1)
        self.spinBox = QtWidgets.QSpinBox(self.errorMapControlsGroupBox)
        self.spinBox.setObjectName("spinBox")
        self.xAxisAndYAxisGridLayout.addWidget(self.spinBox, 2, 3, 1, 1)
        self.pauseAndRezoomErrorMapPushButton = QtWidgets.QPushButton(self.errorMapControlsGroupBox)
        self.pauseAndRezoomErrorMapPushButton.setObjectName("pauseAndRezoomErrorMapPushButton")
        self.xAxisAndYAxisGridLayout.addWidget(self.pauseAndRezoomErrorMapPushButton, 3, 3, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(120, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.xAxisAndYAxisGridLayout.addItem(spacerItem3, 0, 0, 1, 1)
        self.verticalLayout_2.addLayout(self.xAxisAndYAxisGridLayout)
        self.errorMapProgressBar = QtWidgets.QProgressBar(self.errorMapControlsGroupBox)
        self.errorMapProgressBar.setProperty("value", 24)
        self.errorMapProgressBar.setObjectName("errorMapProgressBar")
        self.verticalLayout_2.addWidget(self.errorMapProgressBar)
        self.gridLayout.addWidget(self.errorMapControlsGroupBox, 0, 2, 1, 1)
        self.mainGraphControlsGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.mainGraphControlsGroupBox.setObjectName("mainGraphControlsGroupBox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.mainGraphControlsGroupBox)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.signalCoveragePrecentageLabel = QtWidgets.QLabel(self.mainGraphControlsGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.signalCoveragePrecentageLabel.sizePolicy().hasHeightForWidth())
        self.signalCoveragePrecentageLabel.setSizePolicy(sizePolicy)
        self.signalCoveragePrecentageLabel.setObjectName("signalCoveragePrecentageLabel")
        self.gridLayout_2.addWidget(self.signalCoveragePrecentageLabel, 2, 2, 1, 1)
        self.precentageOfErrorLabel = QtWidgets.QLabel(self.mainGraphControlsGroupBox)
        self.precentageOfErrorLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.precentageOfErrorLabel.setObjectName("precentageOfErrorLabel")
        self.gridLayout_2.addWidget(self.precentageOfErrorLabel, 0, 0, 1, 1)
        self.extrapolationLabel = QtWidgets.QLabel(self.mainGraphControlsGroupBox)
        self.extrapolationLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.extrapolationLabel.setObjectName("extrapolationLabel")
        self.gridLayout_2.addWidget(self.extrapolationLabel, 1, 0, 1, 1)
        self.extrapolationHorizontalSlider = QtWidgets.QSlider(self.mainGraphControlsGroupBox)
        self.extrapolationHorizontalSlider.setMaximum(100)
        self.extrapolationHorizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.extrapolationHorizontalSlider.setObjectName("extrapolationHorizontalSlider")
        self.gridLayout_2.addWidget(self.extrapolationHorizontalSlider, 1, 1, 1, 3)
        spacerItem4 = QtWidgets.QSpacerItem(50, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem4, 2, 3, 1, 1)
        self.precentageOfErrorLcdNumber = QtWidgets.QLCDNumber(self.mainGraphControlsGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(20)
        sizePolicy.setHeightForWidth(self.precentageOfErrorLcdNumber.sizePolicy().hasHeightForWidth())
        self.precentageOfErrorLcdNumber.setSizePolicy(sizePolicy)
        self.precentageOfErrorLcdNumber.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.precentageOfErrorLcdNumber.setObjectName("precentageOfErrorLcdNumber")
        self.gridLayout_2.addWidget(self.precentageOfErrorLcdNumber, 0, 1, 1, 1)
        self.CurveFittingCoveragePrecentageLcdNumber = QtWidgets.QLCDNumber(self.mainGraphControlsGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(40)
        sizePolicy.setVerticalStretch(20)
        sizePolicy.setHeightForWidth(self.CurveFittingCoveragePrecentageLcdNumber.sizePolicy().hasHeightForWidth())
        self.CurveFittingCoveragePrecentageLcdNumber.setSizePolicy(sizePolicy)
        self.CurveFittingCoveragePrecentageLcdNumber.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.CurveFittingCoveragePrecentageLcdNumber.setFocusPolicy(QtCore.Qt.NoFocus)
        self.CurveFittingCoveragePrecentageLcdNumber.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.CurveFittingCoveragePrecentageLcdNumber.setSmallDecimalPoint(False)
        self.CurveFittingCoveragePrecentageLcdNumber.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.CurveFittingCoveragePrecentageLcdNumber.setObjectName("CurveFittingCoveragePrecentageLcdNumber")
        self.gridLayout_2.addWidget(self.CurveFittingCoveragePrecentageLcdNumber, 2, 1, 1, 1)
        self.extrapolationPercentageLabel = QtWidgets.QLabel(self.mainGraphControlsGroupBox)
        self.extrapolationPercentageLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.extrapolationPercentageLabel.setObjectName("extrapolationPercentageLabel")
        self.gridLayout_2.addWidget(self.extrapolationPercentageLabel, 1, 5, 1, 1)
        self.CurveFittingCoveragePrecentageLabel = QtWidgets.QLabel(self.mainGraphControlsGroupBox)
        self.CurveFittingCoveragePrecentageLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.CurveFittingCoveragePrecentageLabel.setObjectName("CurveFittingCoveragePrecentageLabel")
        self.gridLayout_2.addWidget(self.CurveFittingCoveragePrecentageLabel, 2, 0, 1, 1)
        self.precentageLabel = QtWidgets.QLabel(self.mainGraphControlsGroupBox)
        self.precentageLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.precentageLabel.setObjectName("precentageLabel")
        self.gridLayout_2.addWidget(self.precentageLabel, 0, 2, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout_2)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.numberOfChunksSpinBox = QtWidgets.QSpinBox(self.mainGraphControlsGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.numberOfChunksSpinBox.sizePolicy().hasHeightForWidth())
        self.numberOfChunksSpinBox.setSizePolicy(sizePolicy)
        self.numberOfChunksSpinBox.setMinimum(1)
        self.numberOfChunksSpinBox.setMaximum(20)
        self.numberOfChunksSpinBox.setObjectName("numberOfChunksSpinBox")
        self.gridLayout_3.addWidget(self.numberOfChunksSpinBox, 2, 4, 1, 1)
        self.overlappingRadioButton = QtWidgets.QRadioButton(self.mainGraphControlsGroupBox)
        self.overlappingRadioButton.setObjectName("overlappingRadioButton")
        self.gridLayout_3.addWidget(self.overlappingRadioButton, 4, 4, 1, 1)
        self.overlapLabel = QtWidgets.QLabel(self.mainGraphControlsGroupBox)
        self.overlapLabel.setObjectName("overlapLabel")
        self.gridLayout_3.addWidget(self.overlapLabel, 1, 5, 1, 1)
        self.fitPushButton = QtWidgets.QPushButton(self.mainGraphControlsGroupBox)
        self.fitPushButton.setObjectName("fitPushButton")
        self.gridLayout_3.addWidget(self.fitPushButton, 5, 3, 1, 1)
        self.numberOfChunksLabel = QtWidgets.QLabel(self.mainGraphControlsGroupBox)
        self.numberOfChunksLabel.setObjectName("numberOfChunksLabel")
        self.gridLayout_3.addWidget(self.numberOfChunksLabel, 1, 4, 1, 1)
        self.noOverlappingRadioButton = QtWidgets.QRadioButton(self.mainGraphControlsGroupBox)
        self.noOverlappingRadioButton.setObjectName("noOverlappingRadioButton")
        self.gridLayout_3.addWidget(self.noOverlappingRadioButton, 3, 4, 1, 1)
        self.multipleChunksRadioButton = QtWidgets.QRadioButton(self.mainGraphControlsGroupBox)
        self.multipleChunksRadioButton.setObjectName("multipleChunksRadioButton")
        self.gridLayout_3.addWidget(self.multipleChunksRadioButton, 4, 3, 1, 1)
        self.fittingOrderSpinBox = QtWidgets.QSpinBox(self.mainGraphControlsGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(50)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fittingOrderSpinBox.sizePolicy().hasHeightForWidth())
        self.fittingOrderSpinBox.setSizePolicy(sizePolicy)
        self.fittingOrderSpinBox.setMaximum(10)
        self.fittingOrderSpinBox.setObjectName("fittingOrderSpinBox")
        self.gridLayout_3.addWidget(self.fittingOrderSpinBox, 2, 3, 1, 1)
        self.fittingOrderLabel = QtWidgets.QLabel(self.mainGraphControlsGroupBox)
        self.fittingOrderLabel.setObjectName("fittingOrderLabel")
        self.gridLayout_3.addWidget(self.fittingOrderLabel, 1, 3, 1, 1)
        self.oneChunkRadioButton = QtWidgets.QRadioButton(self.mainGraphControlsGroupBox)
        self.oneChunkRadioButton.setObjectName("oneChunkRadioButton")
        self.gridLayout_3.addWidget(self.oneChunkRadioButton, 3, 3, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.mainGraphControlsGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 0, 1, 1, 1)
        self.cubicRadioButton = QtWidgets.QRadioButton(self.mainGraphControlsGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cubicRadioButton.sizePolicy().hasHeightForWidth())
        self.cubicRadioButton.setSizePolicy(sizePolicy)
        self.cubicRadioButton.setObjectName("cubicRadioButton")
        self.gridLayout_3.addWidget(self.cubicRadioButton, 3, 1, 1, 1)
        self.polynomialRadioButton = QtWidgets.QRadioButton(self.mainGraphControlsGroupBox)
        self.polynomialRadioButton.setObjectName("polynomialRadioButton")
        self.gridLayout_3.addWidget(self.polynomialRadioButton, 1, 1, 1, 1)
        self.splineRadioButton = QtWidgets.QRadioButton(self.mainGraphControlsGroupBox)
        self.splineRadioButton.setObjectName("splineRadioButton")
        self.gridLayout_3.addWidget(self.splineRadioButton, 2, 1, 1, 1)
        self.constantChunkRadioButton = QtWidgets.QRadioButton(self.mainGraphControlsGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.constantChunkRadioButton.sizePolicy().hasHeightForWidth())
        self.constantChunkRadioButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setStrikeOut(False)
        self.constantChunkRadioButton.setFont(font)
        self.constantChunkRadioButton.setAutoRepeat(False)
        self.constantChunkRadioButton.setObjectName("constantChunkRadioButton")
        self.gridLayout_3.addWidget(self.constantChunkRadioButton, 3, 5, 1, 1)
        self.overlapSpinBox = QtWidgets.QSpinBox(self.mainGraphControlsGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.overlapSpinBox.sizePolicy().hasHeightForWidth())
        self.overlapSpinBox.setSizePolicy(sizePolicy)
        self.overlapSpinBox.setMaximum(25)
        self.overlapSpinBox.setObjectName("overlapSpinBox")
        self.gridLayout_3.addWidget(self.overlapSpinBox, 2, 5, 1, 1)
        self.fullCoverageRadioButton = QtWidgets.QRadioButton(self.mainGraphControlsGroupBox)
        self.fullCoverageRadioButton.setObjectName("fullCoverageRadioButton")
        self.gridLayout_3.addWidget(self.fullCoverageRadioButton, 4, 5, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout_3)
        self.gridLayout.addWidget(self.mainGraphControlsGroupBox, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1322, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.openAction = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/image/icons/open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.openAction.setIcon(icon)
        self.openAction.setObjectName("openAction")
        self.menuFile.addAction(self.openAction)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.errorMapControlsGroupBox.setTitle(_translate("MainWindow", "Error map controls"))
        self.xAxisComboBox.setItemText(0, _translate("MainWindow", "Choose Axis Parameter"))
        self.xAxisComboBox.setItemText(1, _translate("MainWindow", "Polynomial Order"))
        self.xAxisComboBox.setItemText(2, _translate("MainWindow", "Number of Chunks"))
        self.xAxisComboBox.setItemText(3, _translate("MainWindow", "Overlapping Percentage"))
        self.startAndCancelErrorMapPushButton.setText(_translate("MainWindow", "Start"))
        self.xAxisLabel.setText(_translate("MainWindow", "X-axis"))
        self.yAxisComboBox.setItemText(0, _translate("MainWindow", "Choose Axis Parameter"))
        self.yAxisComboBox.setItemText(1, _translate("MainWindow", "Polynomial Order"))
        self.yAxisComboBox.setItemText(2, _translate("MainWindow", "Number of Chunks"))
        self.yAxisComboBox.setItemText(3, _translate("MainWindow", "Overlapping Percentage"))
        self.label.setText(_translate("MainWindow", "Constant Parameter"))
        self.yAxisLabel.setText(_translate("MainWindow", "Y-axis"))
        self.pauseAndRezoomErrorMapPushButton.setText(_translate("MainWindow", "Pause"))
        self.mainGraphControlsGroupBox.setTitle(_translate("MainWindow", "Main Graph Controls"))
        self.signalCoveragePrecentageLabel.setText(_translate("MainWindow", "%"))
        self.precentageOfErrorLabel.setText(_translate("MainWindow", "Percentage of Error"))
        self.extrapolationLabel.setText(_translate("MainWindow", "Extrapolation"))
        self.extrapolationPercentageLabel.setText(_translate("MainWindow", "0% Original Signal"))
        self.CurveFittingCoveragePrecentageLabel.setText(_translate("MainWindow", "Signal curve fitting coverage"))
        self.precentageLabel.setText(_translate("MainWindow", "%"))
        self.overlappingRadioButton.setText(_translate("MainWindow", "Overlapping"))
        self.overlapLabel.setText(_translate("MainWindow", "Overlapping Percentage"))
        self.fitPushButton.setText(_translate("MainWindow", "Fit"))
        self.numberOfChunksLabel.setText(_translate("MainWindow", "Number of chunks"))
        self.noOverlappingRadioButton.setText(_translate("MainWindow", "No Overlapping"))
        self.multipleChunksRadioButton.setText(_translate("MainWindow", "Multiple Chunks"))
        self.fittingOrderLabel.setText(_translate("MainWindow", "Fitting order"))
        self.oneChunkRadioButton.setText(_translate("MainWindow", "One Chunk"))
        self.label_2.setText(_translate("MainWindow", "Interpolation Methods"))
        self.cubicRadioButton.setText(_translate("MainWindow", "Cubic"))
        self.polynomialRadioButton.setText(_translate("MainWindow", "Polynomial"))
        self.splineRadioButton.setText(_translate("MainWindow", "Spline"))
        self.constantChunkRadioButton.setText(_translate("MainWindow", "Keep user input\'s number of chunks constant"))
        self.fullCoverageRadioButton.setText(_translate("MainWindow", "Keep 100% signal curve fitting coverage"))
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
