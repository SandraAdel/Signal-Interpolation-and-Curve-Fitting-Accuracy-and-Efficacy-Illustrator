# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\spring22\SBEN311\TASKSS\task#4\Interpolation-Curve-Fitting-App\GUI2.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1470, 1044)
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
        self.latexEquationLabel.setObjectName("latexEquationLabel")
        self.gridLayout_4.addWidget(self.latexEquationLabel, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_4)
        self.mainGraphAndErrorMapGridLayout = QtWidgets.QGridLayout()
        self.mainGraphAndErrorMapGridLayout.setObjectName("mainGraphAndErrorMapGridLayout")
        spacerItem = QtWidgets.QSpacerItem(0, 300, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.mainGraphAndErrorMapGridLayout.addItem(spacerItem, 0, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(850, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.mainGraphAndErrorMapGridLayout.addItem(spacerItem1, 1, 0, 1, 1)
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
        self.verticalLayout.addLayout(self.mainGraphAndErrorMapGridLayout)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        spacerItem2 = QtWidgets.QSpacerItem(20, 500, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem2, 0, 1, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 2, 1, 1, 1)
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
        self.xAxisLabel = QtWidgets.QLabel(self.errorMapControlsGroupBox)
        self.xAxisLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.xAxisLabel.setObjectName("xAxisLabel")
        self.xAxisAndYAxisGridLayout.addWidget(self.xAxisLabel, 0, 0, 1, 1)
        self.xAxisComboBox = QtWidgets.QComboBox(self.errorMapControlsGroupBox)
        self.xAxisComboBox.setObjectName("xAxisComboBox")
        self.xAxisComboBox.addItem("")
        self.xAxisComboBox.addItem("")
        self.xAxisAndYAxisGridLayout.addWidget(self.xAxisComboBox, 0, 2, 1, 1)
        self.yAxisLabel = QtWidgets.QLabel(self.errorMapControlsGroupBox)
        self.yAxisLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.yAxisLabel.setObjectName("yAxisLabel")
        self.xAxisAndYAxisGridLayout.addWidget(self.yAxisLabel, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.errorMapControlsGroupBox)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.xAxisAndYAxisGridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.yAxisComboBox = QtWidgets.QComboBox(self.errorMapControlsGroupBox)
        self.yAxisComboBox.setObjectName("yAxisComboBox")
        self.yAxisComboBox.addItem("")
        self.yAxisComboBox.addItem("")
        self.xAxisAndYAxisGridLayout.addWidget(self.yAxisComboBox, 1, 2, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(120, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.xAxisAndYAxisGridLayout.addItem(spacerItem4, 0, 3, 1, 1)
        self.startAndCancelErrorMapPushButton = QtWidgets.QPushButton(self.errorMapControlsGroupBox)
        self.startAndCancelErrorMapPushButton.setObjectName("startAndCancelErrorMapPushButton")
        self.xAxisAndYAxisGridLayout.addWidget(self.startAndCancelErrorMapPushButton, 3, 0, 1, 1)
        self.pauseAndRezoomErrorMapPushButton = QtWidgets.QPushButton(self.errorMapControlsGroupBox)
        self.pauseAndRezoomErrorMapPushButton.setObjectName("pauseAndRezoomErrorMapPushButton")
        self.xAxisAndYAxisGridLayout.addWidget(self.pauseAndRezoomErrorMapPushButton, 3, 2, 1, 1)
        self.spinBox = QtWidgets.QSpinBox(self.errorMapControlsGroupBox)
        self.spinBox.setObjectName("spinBox")
        self.xAxisAndYAxisGridLayout.addWidget(self.spinBox, 2, 2, 1, 1)
        self.verticalLayout_2.addLayout(self.xAxisAndYAxisGridLayout)
        self.errorMapProgressBar = QtWidgets.QProgressBar(self.errorMapControlsGroupBox)
        self.errorMapProgressBar.setProperty("value", 24)
        self.errorMapProgressBar.setObjectName("errorMapProgressBar")
        self.verticalLayout_2.addWidget(self.errorMapProgressBar)
        self.gridLayout.addWidget(self.errorMapControlsGroupBox, 0, 3, 1, 1)
        self.mainGraphControlsGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.mainGraphControlsGroupBox.setObjectName("mainGraphControlsGroupBox")
        self.layoutWidget = QtWidgets.QWidget(self.mainGraphControlsGroupBox)
        self.layoutWidget.setGeometry(QtCore.QRect(160, 20, 481, 61))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.extrapolationLabel = QtWidgets.QLabel(self.layoutWidget)
        self.extrapolationLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.extrapolationLabel.setObjectName("extrapolationLabel")
        self.gridLayout_2.addWidget(self.extrapolationLabel, 0, 0, 1, 1)
        self.extrapolationHorizontalSlider = QtWidgets.QSlider(self.layoutWidget)
        self.extrapolationHorizontalSlider.setMaximum(100)
        self.extrapolationHorizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.extrapolationHorizontalSlider.setObjectName("extrapolationHorizontalSlider")
        self.gridLayout_2.addWidget(self.extrapolationHorizontalSlider, 0, 1, 1, 1)
        self.extrapolationPercentageLabel = QtWidgets.QLabel(self.layoutWidget)
        self.extrapolationPercentageLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.extrapolationPercentageLabel.setObjectName("extrapolationPercentageLabel")
        self.gridLayout_2.addWidget(self.extrapolationPercentageLabel, 0, 2, 1, 1)
        self.CurveFittingCoveragePrecentageLabel = QtWidgets.QLabel(self.layoutWidget)
        self.CurveFittingCoveragePrecentageLabel.setObjectName("CurveFittingCoveragePrecentageLabel")
        self.gridLayout_2.addWidget(self.CurveFittingCoveragePrecentageLabel, 1, 0, 1, 1)
        self.CurveFittingCoveragePrecentageLcdNumber = QtWidgets.QLCDNumber(self.layoutWidget)
        self.CurveFittingCoveragePrecentageLcdNumber.setObjectName("CurveFittingCoveragePrecentageLcdNumber")
        self.gridLayout_2.addWidget(self.CurveFittingCoveragePrecentageLcdNumber, 1, 1, 1, 1)
        self.signalCoveragePrecentageLabel = QtWidgets.QLabel(self.layoutWidget)
        self.signalCoveragePrecentageLabel.setObjectName("signalCoveragePrecentageLabel")
        self.gridLayout_2.addWidget(self.signalCoveragePrecentageLabel, 1, 2, 1, 1)
        self.layoutWidget1 = QtWidgets.QWidget(self.mainGraphControlsGroupBox)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 100, 865, 401))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.layoutWidget1)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.polynomialFittingOrderSpinBox = QtWidgets.QSpinBox(self.layoutWidget1)
        self.polynomialFittingOrderSpinBox.setMaximum(10)
        self.polynomialFittingOrderSpinBox.setObjectName("polynomialFittingOrderSpinBox")
        self.gridLayout_3.addWidget(self.polynomialFittingOrderSpinBox, 2, 2, 1, 1)
        self.polynomialFittingOrderLabel = QtWidgets.QLabel(self.layoutWidget1)
        self.polynomialFittingOrderLabel.setObjectName("polynomialFittingOrderLabel")
        self.gridLayout_3.addWidget(self.polynomialFittingOrderLabel, 1, 2, 1, 1)
        self.polynomialFitPushButton = QtWidgets.QPushButton(self.layoutWidget1)
        self.polynomialFitPushButton.setObjectName("polynomialFitPushButton")
        self.gridLayout_3.addWidget(self.polynomialFitPushButton, 13, 2, 1, 1)
        self.polynomialOverlapLabel = QtWidgets.QLabel(self.layoutWidget1)
        self.polynomialOverlapLabel.setObjectName("polynomialOverlapLabel")
        self.gridLayout_3.addWidget(self.polynomialOverlapLabel, 9, 2, 1, 1)
        self.polynomialOverlapSpinBox = QtWidgets.QSpinBox(self.layoutWidget1)
        self.polynomialOverlapSpinBox.setMaximum(25)
        self.polynomialOverlapSpinBox.setObjectName("polynomialOverlapSpinBox")
        self.gridLayout_3.addWidget(self.polynomialOverlapSpinBox, 10, 2, 1, 1)
        self.polynomialRadioButton = QtWidgets.QRadioButton(self.layoutWidget1)
        self.polynomialRadioButton.setObjectName("polynomialRadioButton")
        self.gridLayout_3.addWidget(self.polynomialRadioButton, 0, 2, 1, 1)
        self.polynomialConstantChunkRadioButton = QtWidgets.QRadioButton(self.layoutWidget1)
        font = QtGui.QFont()
        font.setStrikeOut(False)
        self.polynomialConstantChunkRadioButton.setFont(font)
        self.polynomialConstantChunkRadioButton.setAutoRepeat(False)
        self.polynomialConstantChunkRadioButton.setObjectName("polynomialConstantChunkRadioButton")
        self.gridLayout_3.addWidget(self.polynomialConstantChunkRadioButton, 11, 2, 1, 1)
        self.cubicRadioButton = QtWidgets.QRadioButton(self.layoutWidget1)
        self.cubicRadioButton.setObjectName("cubicRadioButton")
        self.gridLayout_3.addWidget(self.cubicRadioButton, 0, 0, 1, 1)
        self.splineRadioButton = QtWidgets.QRadioButton(self.layoutWidget1)
        self.splineRadioButton.setObjectName("splineRadioButton")
        self.gridLayout_3.addWidget(self.splineRadioButton, 0, 1, 1, 1)
        self.polynomialOneChunkRadioButton = QtWidgets.QRadioButton(self.layoutWidget1)
        self.polynomialOneChunkRadioButton.setObjectName("polynomialOneChunkRadioButton")
        self.gridLayout_3.addWidget(self.polynomialOneChunkRadioButton, 3, 2, 1, 1)
        self.polynomialNumberOfChunksSpinBox = QtWidgets.QSpinBox(self.layoutWidget1)
        self.polynomialNumberOfChunksSpinBox.setMinimum(1)
        self.polynomialNumberOfChunksSpinBox.setMaximum(20)
        self.polynomialNumberOfChunksSpinBox.setObjectName("polynomialNumberOfChunksSpinBox")
        self.gridLayout_3.addWidget(self.polynomialNumberOfChunksSpinBox, 6, 2, 1, 1)
        self.polynomialOverlappingRadioButton = QtWidgets.QRadioButton(self.layoutWidget1)
        self.polynomialOverlappingRadioButton.setObjectName("polynomialOverlappingRadioButton")
        self.gridLayout_3.addWidget(self.polynomialOverlappingRadioButton, 8, 2, 1, 1)
        self.polynomialNoOverlappingRadioButton = QtWidgets.QRadioButton(self.layoutWidget1)
        self.polynomialNoOverlappingRadioButton.setObjectName("polynomialNoOverlappingRadioButton")
        self.gridLayout_3.addWidget(self.polynomialNoOverlappingRadioButton, 7, 2, 1, 1)
        self.polynomialFullCoverageRadioButton = QtWidgets.QRadioButton(self.layoutWidget1)
        self.polynomialFullCoverageRadioButton.setObjectName("polynomialFullCoverageRadioButton")
        self.gridLayout_3.addWidget(self.polynomialFullCoverageRadioButton, 12, 2, 1, 1)
        self.polynomialMultipleChunksRadioButton = QtWidgets.QRadioButton(self.layoutWidget1)
        self.polynomialMultipleChunksRadioButton.setObjectName("polynomialMultipleChunksRadioButton")
        self.gridLayout_3.addWidget(self.polynomialMultipleChunksRadioButton, 4, 2, 1, 1)
        self.polynomialNumberOfChunksLabel = QtWidgets.QLabel(self.layoutWidget1)
        self.polynomialNumberOfChunksLabel.setObjectName("polynomialNumberOfChunksLabel")
        self.gridLayout_3.addWidget(self.polynomialNumberOfChunksLabel, 5, 2, 1, 1)
        self.cubicOneChunkRadioButton = QtWidgets.QRadioButton(self.layoutWidget1)
        self.cubicOneChunkRadioButton.setObjectName("cubicOneChunkRadioButton")
        self.gridLayout_3.addWidget(self.cubicOneChunkRadioButton, 1, 0, 1, 1)
        self.cubicMultipleChunksRadioButton = QtWidgets.QRadioButton(self.layoutWidget1)
        self.cubicMultipleChunksRadioButton.setObjectName("cubicMultipleChunksRadioButton")
        self.gridLayout_3.addWidget(self.cubicMultipleChunksRadioButton, 2, 0, 1, 1)
        self.cubicNumberOfChunksLabel = QtWidgets.QLabel(self.layoutWidget1)
        self.cubicNumberOfChunksLabel.setObjectName("cubicNumberOfChunksLabel")
        self.gridLayout_3.addWidget(self.cubicNumberOfChunksLabel, 3, 0, 1, 1)
        self.cubicNumberOfChunksSpinBox = QtWidgets.QSpinBox(self.layoutWidget1)
        self.cubicNumberOfChunksSpinBox.setMinimum(1)
        self.cubicNumberOfChunksSpinBox.setMaximum(20)
        self.cubicNumberOfChunksSpinBox.setObjectName("cubicNumberOfChunksSpinBox")
        self.gridLayout_3.addWidget(self.cubicNumberOfChunksSpinBox, 4, 0, 1, 1)
        self.cubicNoOverlappingRadioButton = QtWidgets.QRadioButton(self.layoutWidget1)
        self.cubicNoOverlappingRadioButton.setObjectName("cubicNoOverlappingRadioButton")
        self.gridLayout_3.addWidget(self.cubicNoOverlappingRadioButton, 5, 0, 1, 1)
        self.cubicOverlappingRadioButton = QtWidgets.QRadioButton(self.layoutWidget1)
        self.cubicOverlappingRadioButton.setObjectName("cubicOverlappingRadioButton")
        self.gridLayout_3.addWidget(self.cubicOverlappingRadioButton, 6, 0, 1, 1)
        self.cubicOverlapLabel = QtWidgets.QLabel(self.layoutWidget1)
        self.cubicOverlapLabel.setObjectName("cubicOverlapLabel")
        self.gridLayout_3.addWidget(self.cubicOverlapLabel, 7, 0, 1, 1)
        self.cubicOverlapSpinBox = QtWidgets.QSpinBox(self.layoutWidget1)
        self.cubicOverlapSpinBox.setMaximum(25)
        self.cubicOverlapSpinBox.setObjectName("cubicOverlapSpinBox")
        self.gridLayout_3.addWidget(self.cubicOverlapSpinBox, 8, 0, 1, 1)
        self.cubicConstantChunkRadioButton = QtWidgets.QRadioButton(self.layoutWidget1)
        font = QtGui.QFont()
        font.setStrikeOut(False)
        self.cubicConstantChunkRadioButton.setFont(font)
        self.cubicConstantChunkRadioButton.setAutoRepeat(False)
        self.cubicConstantChunkRadioButton.setObjectName("cubicConstantChunkRadioButton")
        self.gridLayout_3.addWidget(self.cubicConstantChunkRadioButton, 9, 0, 1, 1)
        self.cubicFullCoverageRadioButton = QtWidgets.QRadioButton(self.layoutWidget1)
        self.cubicFullCoverageRadioButton.setObjectName("cubicFullCoverageRadioButton")
        self.gridLayout_3.addWidget(self.cubicFullCoverageRadioButton, 10, 0, 1, 1)
        self.cubicFitPushButton = QtWidgets.QPushButton(self.layoutWidget1)
        self.cubicFitPushButton.setObjectName("cubicFitPushButton")
        self.gridLayout_3.addWidget(self.cubicFitPushButton, 11, 0, 1, 1)
        self.splineFitPushButton = QtWidgets.QPushButton(self.layoutWidget1)
        self.splineFitPushButton.setObjectName("splineFitPushButton")
        self.gridLayout_3.addWidget(self.splineFitPushButton, 13, 1, 1, 1)
        self.splineFullCoverageRadioButton = QtWidgets.QRadioButton(self.layoutWidget1)
        self.splineFullCoverageRadioButton.setObjectName("splineFullCoverageRadioButton")
        self.gridLayout_3.addWidget(self.splineFullCoverageRadioButton, 12, 1, 1, 1)
        self.splineConstantChunkRadioButton = QtWidgets.QRadioButton(self.layoutWidget1)
        font = QtGui.QFont()
        font.setStrikeOut(False)
        self.splineConstantChunkRadioButton.setFont(font)
        self.splineConstantChunkRadioButton.setAutoRepeat(False)
        self.splineConstantChunkRadioButton.setObjectName("splineConstantChunkRadioButton")
        self.gridLayout_3.addWidget(self.splineConstantChunkRadioButton, 11, 1, 1, 1)
        self.splineOverlapSpinBox = QtWidgets.QSpinBox(self.layoutWidget1)
        self.splineOverlapSpinBox.setMaximum(25)
        self.splineOverlapSpinBox.setObjectName("splineOverlapSpinBox")
        self.gridLayout_3.addWidget(self.splineOverlapSpinBox, 10, 1, 1, 1)
        self.splineOverlapLabel = QtWidgets.QLabel(self.layoutWidget1)
        self.splineOverlapLabel.setObjectName("splineOverlapLabel")
        self.gridLayout_3.addWidget(self.splineOverlapLabel, 9, 1, 1, 1)
        self.splineOverlappingRadioButton = QtWidgets.QRadioButton(self.layoutWidget1)
        self.splineOverlappingRadioButton.setObjectName("splineOverlappingRadioButton")
        self.gridLayout_3.addWidget(self.splineOverlappingRadioButton, 8, 1, 1, 1)
        self.splineNoOverlappingRadioButton = QtWidgets.QRadioButton(self.layoutWidget1)
        self.splineNoOverlappingRadioButton.setObjectName("splineNoOverlappingRadioButton")
        self.gridLayout_3.addWidget(self.splineNoOverlappingRadioButton, 7, 1, 1, 1)
        self.splineNumberOfChunksSpinBox = QtWidgets.QSpinBox(self.layoutWidget1)
        self.splineNumberOfChunksSpinBox.setMinimum(1)
        self.splineNumberOfChunksSpinBox.setMaximum(20)
        self.splineNumberOfChunksSpinBox.setObjectName("splineNumberOfChunksSpinBox")
        self.gridLayout_3.addWidget(self.splineNumberOfChunksSpinBox, 6, 1, 1, 1)
        self.splineNumberOfChunksLabel = QtWidgets.QLabel(self.layoutWidget1)
        self.splineNumberOfChunksLabel.setObjectName("splineNumberOfChunksLabel")
        self.gridLayout_3.addWidget(self.splineNumberOfChunksLabel, 5, 1, 1, 1)
        self.splineMultipleChunksRadioButton = QtWidgets.QRadioButton(self.layoutWidget1)
        self.splineMultipleChunksRadioButton.setObjectName("splineMultipleChunksRadioButton")
        self.gridLayout_3.addWidget(self.splineMultipleChunksRadioButton, 4, 1, 1, 1)
        self.splineOneChunkRadioButton = QtWidgets.QRadioButton(self.layoutWidget1)
        self.splineOneChunkRadioButton.setObjectName("splineOneChunkRadioButton")
        self.gridLayout_3.addWidget(self.splineOneChunkRadioButton, 3, 1, 1, 1)
        self.splineFittingOrderSpinBox = QtWidgets.QSpinBox(self.layoutWidget1)
        self.splineFittingOrderSpinBox.setMaximum(10)
        self.splineFittingOrderSpinBox.setObjectName("splineFittingOrderSpinBox")
        self.gridLayout_3.addWidget(self.splineFittingOrderSpinBox, 2, 1, 1, 1)
        self.splineFittingOrderLabel = QtWidgets.QLabel(self.layoutWidget1)
        self.splineFittingOrderLabel.setObjectName("splineFittingOrderLabel")
        self.gridLayout_3.addWidget(self.splineFittingOrderLabel, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.mainGraphControlsGroupBox, 0, 0, 2, 1)
        spacerItem5 = QtWidgets.QSpacerItem(880, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem5, 2, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1470, 26))
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
        self.latexEquationLabel.setText(_translate("MainWindow", "Latex equation"))
        self.errorMapControlsGroupBox.setTitle(_translate("MainWindow", "Error map controls"))
        self.xAxisLabel.setText(_translate("MainWindow", "X-axis"))
        self.xAxisComboBox.setItemText(0, _translate("MainWindow", "Polynomial Order"))
        self.xAxisComboBox.setItemText(1, _translate("MainWindow", "Overlapping Percentage"))
        self.yAxisLabel.setText(_translate("MainWindow", "Y-axis"))
        self.label.setText(_translate("MainWindow", "Constant Parameter"))
        self.yAxisComboBox.setItemText(0, _translate("MainWindow", "Number of Chunks"))
        self.yAxisComboBox.setItemText(1, _translate("MainWindow", "Overlapping Percentage"))
        self.startAndCancelErrorMapPushButton.setText(_translate("MainWindow", "Start"))
        self.pauseAndRezoomErrorMapPushButton.setText(_translate("MainWindow", "Pause"))
        self.mainGraphControlsGroupBox.setTitle(_translate("MainWindow", "Main Graph Controls"))
        self.extrapolationLabel.setText(_translate("MainWindow", "Extrapolation"))
        self.extrapolationPercentageLabel.setText(_translate("MainWindow", "0% Original Signal"))
        self.CurveFittingCoveragePrecentageLabel.setText(_translate("MainWindow", "Signal curve fitting coverage"))
        self.signalCoveragePrecentageLabel.setText(_translate("MainWindow", "%"))
        self.polynomialFittingOrderLabel.setText(_translate("MainWindow", "Fitting order"))
        self.polynomialFitPushButton.setText(_translate("MainWindow", "Fit"))
        self.polynomialOverlapLabel.setText(_translate("MainWindow", "overlap"))
        self.polynomialRadioButton.setText(_translate("MainWindow", "Polynomial"))
        self.polynomialConstantChunkRadioButton.setText(_translate("MainWindow", "Keep user input\'s number of chunks constant"))
        self.cubicRadioButton.setText(_translate("MainWindow", "Cubic"))
        self.splineRadioButton.setText(_translate("MainWindow", "Spline"))
        self.polynomialOneChunkRadioButton.setText(_translate("MainWindow", "One Chunk"))
        self.polynomialOverlappingRadioButton.setText(_translate("MainWindow", "Overlapping"))
        self.polynomialNoOverlappingRadioButton.setText(_translate("MainWindow", "No Overlapping"))
        self.polynomialFullCoverageRadioButton.setText(_translate("MainWindow", "Keep 100% signal curve fitting coverage"))
        self.polynomialMultipleChunksRadioButton.setText(_translate("MainWindow", "Multiple Chunks"))
        self.polynomialNumberOfChunksLabel.setText(_translate("MainWindow", "Number of chunks"))
        self.cubicOneChunkRadioButton.setText(_translate("MainWindow", "One Chunk"))
        self.cubicMultipleChunksRadioButton.setText(_translate("MainWindow", "Multiple Chunks"))
        self.cubicNumberOfChunksLabel.setText(_translate("MainWindow", "Number of Chunks"))
        self.cubicNoOverlappingRadioButton.setText(_translate("MainWindow", "No Overlapping"))
        self.cubicOverlappingRadioButton.setText(_translate("MainWindow", "Overlapping"))
        self.cubicOverlapLabel.setText(_translate("MainWindow", "overlap"))
        self.cubicConstantChunkRadioButton.setText(_translate("MainWindow", "Keep user input\'s number of chunks constant"))
        self.cubicFullCoverageRadioButton.setText(_translate("MainWindow", "Keep 100% signal curve fitting coverage"))
        self.cubicFitPushButton.setText(_translate("MainWindow", "Fit"))
        self.splineFitPushButton.setText(_translate("MainWindow", "Fit"))
        self.splineFullCoverageRadioButton.setText(_translate("MainWindow", "Keep 100% signal curve fitting coverage"))
        self.splineConstantChunkRadioButton.setText(_translate("MainWindow", "Keep user input\'s number of chunks constant"))
        self.splineOverlapLabel.setText(_translate("MainWindow", "overlap"))
        self.splineOverlappingRadioButton.setText(_translate("MainWindow", "Overlapping"))
        self.splineNoOverlappingRadioButton.setText(_translate("MainWindow", "No Overlapping"))
        self.splineNumberOfChunksLabel.setText(_translate("MainWindow", "Number of Chunks"))
        self.splineMultipleChunksRadioButton.setText(_translate("MainWindow", "Multiple Chunks"))
        self.splineOneChunkRadioButton.setText(_translate("MainWindow", "One Chunk"))
        self.splineFittingOrderLabel.setText(_translate("MainWindow", "Fitting order"))
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
