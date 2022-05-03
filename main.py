from ast import increment_lineno
from math import ceil
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import pyqtgraph
from pyqtgraph import PlotWidget
import pandas as pd
import numpy as np
from sympy import rad
import more_itertools as mit
from GUI import Ui_MainWindow


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Variables Initialization
        self.TimeReadings = []
        self.AmplitudeReadings = []
        # self.data_frame = [0,0]
        self.signalPoint = 1000
        self.chunkSize = 0
        self.oneChunk = 0
        self.result = []

        self.ui.polynomialNumberOfChunksSpinBox.setValue(1)
        # Hide error map elements
        self.ui.errorMapGraphicsView.hide()
        self.ui.errorLabel.hide()
        self.ui.errorMapProgressBar.hide()
        # Hide polynomial controls 
        self.ui.polynomialFitPushButton.hide()
        self.ui.polynomialFittingOrderLabel.hide()
        self.ui.polynomialFittingOrderSpinBox.hide()
        self.ui.polynomialNumberOfChunksLabel.hide()
        self.ui.polynomialNumberOfChunksSpinBox.hide()
        self.ui.polynomialOerlapSpinBox.hide()
        self.ui.polynomialOverlapLabel.hide()
        self.ui.polynomialOneChunkRadioButton.hide()
        self.ui.polynomialMultipleChunksRadioButton.hide()
        self.ui.polynomialConstantChunkRadioButton.hide()
        self.ui.polynomialOverlapLabel.hide()
        self.ui.polynomialOverlappingPrecentageLabel.hide()
        self.ui.polynomialNoOverlappingRadioButton.hide()
        self.ui.polynomialOverlappingRadioButton.hide()
        self.ui.polynomialFullCoverageRadioButton.hide()
        self.ui.polynomialCurveFittingCoveragePrecentageLabel.hide()
        self.ui.polynomialCurveFittingCoveragePrecentageLcdNumber.hide()
        self.ui.polynomialCurveFittingPrecentageLabel.hide()

        self.ui.cubicSplineFittingOrderLabel.hide()
        self.ui.cubicSplineFittingOrderSpinBox.hide()
        
        # Links of GUI Elements to Methods:
        self.ui.openAction.triggered.connect(lambda: self.OpenFile())
        self.ui.polynomialMultipleChunksRadioButton.toggled.connect(lambda: self.polynomialRadioButtonMultiple())
        self.ui.polynomialOneChunkRadioButton.toggled.connect(lambda: self.polynomialRadioButtonOne())
        self.ui.polynomialRadioButton.toggled.connect(lambda: self.polynomial())
        self.ui.cubicSplineRadioButton.toggled.connect(lambda: self.cubicSpline())
        self.ui.bicubicRadioButton.toggled.connect(lambda: self.bicubic())
        self.ui.polynomialFitPushButton.clicked.connect(lambda: self.interpolation())
        self.ui.extrapolationHorizontalSlider.valueChanged.connect(lambda: self.extrapolation())
        self.ui.xAxisComboBox.currentIndexChanged.connect(lambda: self.xAxis())
        self.ui.polynomialOverlappingRadioButton.toggled.connect(lambda: self.polynomialOverlapRadioButton())
        self.ui.polynomialNoOverlappingRadioButton.toggled.connect(lambda: self.polynomialNoOverlapRadioButton())
        self.ui.polynomialConstantChunkRadioButton.toggled.connect(lambda: self.keepConstantChunkRadioButton())
        self.ui.polynomialFullCoverageRadioButton.toggled.connect(lambda: self.FullCoverageRadioButton())

    # Methods
    def OpenFile(self):
        self.file_name = QtWidgets.QFileDialog.getOpenFileName(caption="Choose Signal", directory="", filter="csv (*.csv)")[0]
        self.data_frame = pd.read_csv(self.file_name, encoding = 'utf-8').fillna(0)
        self.TimeReadings = self.data_frame.iloc[:,0].to_numpy()
        self.AmplitudeReadings = self.data_frame.iloc[:,1].to_numpy()
        self.ui.mainGraphGraphicsView.plot(self.TimeReadings, self.AmplitudeReadings, pen=pyqtgraph.mkPen('b', width=1.5))
            
    #! COODE REPETITION TACK CAAAAAAAAAAAAAAARE 

    def polynomial(self):
        if self.ui.polynomialRadioButton.isChecked():
            # self.ui.polynomialOneChunkRadioButton.show()
            self.ui.polynomialMultipleChunksRadioButton.show()
            self.ui.polynomialFitPushButton.show()
            self.ui.polynomialFittingOrderLabel.show()
            self.ui.polynomialFittingOrderSpinBox.show()
            self.ui.polynomialCurveFittingCoveragePrecentageLabel.show()
            self.ui.polynomialCurveFittingCoveragePrecentageLcdNumber.show()
            self.ui.polynomialCurveFittingPrecentageLabel.show()

            self.ui.cubicSplineFittingOrderLabel.hide()
            self.ui.cubicSplineFittingOrderSpinBox.hide()

    def polynomialRadioButtonMultiple (self):
        if self.ui.polynomialMultipleChunksRadioButton.isChecked():
            self.ui.polynomialOneChunkRadioButton.show()
            self.ui.polynomialNumberOfChunksLabel.show()
            self.ui.polynomialNumberOfChunksSpinBox.show()
            self.ui.polynomialCurveFittingCoveragePrecentageLabel.show()
            self.ui.polynomialCurveFittingCoveragePrecentageLcdNumber.show()
            self.ui.polynomialCurveFittingPrecentageLabel.show()
            # self.ui.polynomialNoOverlappingRadioButton.show()
            self.ui.polynomialOverlappingRadioButton.show()
            
    def polynomialRadioButtonOne (self):
        if self.ui.polynomialOneChunkRadioButton.isChecked():
            self.ui.polynomialNumberOfChunksLabel.hide()
            self.ui.polynomialNumberOfChunksSpinBox.hide()
            self.ui.polynomialOerlapSpinBox.hide()
            self.ui.polynomialOverlapLabel.hide()
            self.ui.polynomialNoOverlappingRadioButton.hide()
            self.ui.polynomialOverlappingRadioButton.hide()
            self.ui.polynomialOerlapSpinBox.hide()
            self.ui.polynomialOverlapLabel.hide()
            self.ui.polynomialFullCoverageRadioButton.hide()
            self.ui.polynomialConstantChunkRadioButton.hide()

    def polynomialOverlapRadioButton(self):
        if self.ui.polynomialOverlappingRadioButton.isChecked():
            self.ui.polynomialOerlapSpinBox.show()
            self.ui.polynomialOverlapLabel.show()
            self.ui.polynomialFullCoverageRadioButton.show()
            self.ui.polynomialConstantChunkRadioButton.show()
            self.ui.polynomialNoOverlappingRadioButton.show()

    def polynomialNoOverlapRadioButton(self):
        if self.ui.polynomialNoOverlappingRadioButton.isChecked():
            self.ui.polynomialOerlapSpinBox.hide()
            self.ui.polynomialOverlapLabel.hide()
            self.ui.polynomialFullCoverageRadioButton.hide()
            self.ui.polynomialConstantChunkRadioButton.hide()
    
    def cubicSpline(self):
        if self.ui.cubicSplineRadioButton.isChecked():
            self.ui.cubicSplineFittingOrderLabel.show()
            self.ui.cubicSplineFittingOrderSpinBox.show()

            self.ui.polynomialOneChunkRadioButton.hide()
            self.ui.polynomialMultipleChunksRadioButton.hide()
            self.ui.polynomialFitPushButton.hide()
            self.ui.polynomialFittingOrderLabel.hide()
            self.ui.polynomialFittingOrderSpinBox.hide()
            self.ui.polynomialNumberOfChunksLabel.hide()
            self.ui.polynomialNumberOfChunksSpinBox.hide()
            self.ui.polynomialOerlapSpinBox.hide()
            self.ui.polynomialOverlapLabel.hide()
            self.ui.polynomialCurveFittingCoveragePrecentageLabel.hide()
            self.ui.polynomialCurveFittingCoveragePrecentageLcdNumber.hide()
            self.ui.polynomialCurveFittingPrecentageLabel.hide()
            self.ui.polynomialNumberOfChunksLabel.hide()
            self.ui.polynomialNumberOfChunksSpinBox.hide()
            self.ui.polynomialOerlapSpinBox.hide()
            self.ui.polynomialOverlapLabel.hide()
            self.ui.polynomialNoOverlappingRadioButton.hide()
            self.ui.polynomialOverlappingRadioButton.hide()
            self.ui.polynomialOerlapSpinBox.hide()
            self.ui.polynomialOverlapLabel.hide()
            self.ui.polynomialFullCoverageRadioButton.hide()
            self.ui.polynomialConstantChunkRadioButton.hide()

    def bicubic(self):
        if self.ui.bicubicRadioButton.isChecked():
            
            self.ui.cubicSplineFittingOrderLabel.hide()
            self.ui.cubicSplineFittingOrderSpinBox.hide()

            self.ui.polynomialOneChunkRadioButton.hide()
            self.ui.polynomialMultipleChunksRadioButton.hide()
            self.ui.polynomialFitPushButton.hide()
            self.ui.polynomialFittingOrderLabel.hide()
            self.ui.polynomialFittingOrderSpinBox.hide()
            self.ui.polynomialNumberOfChunksLabel.hide()
            self.ui.polynomialNumberOfChunksSpinBox.hide()
            self.ui.polynomialOerlapSpinBox.hide()
            self.ui.polynomialOverlapLabel.hide()
            self.ui.polynomialCurveFittingCoveragePrecentageLabel.hide()
            self.ui.polynomialCurveFittingCoveragePrecentageLcdNumber.hide()
            self.ui.polynomialCurveFittingPrecentageLabel.hide()
            self.ui.polynomialNumberOfChunksLabel.hide()
            self.ui.polynomialNumberOfChunksSpinBox.hide()
            self.ui.polynomialOerlapSpinBox.hide()
            self.ui.polynomialOverlapLabel.hide()
            self.ui.polynomialNoOverlappingRadioButton.hide()
            self.ui.polynomialOverlappingRadioButton.hide()
            self.ui.polynomialOerlapSpinBox.hide()
            self.ui.polynomialOverlapLabel.hide()
            self.ui.polynomialFullCoverageRadioButton.hide()
            self.ui.polynomialConstantChunkRadioButton.hide()

    def xAxis(self):
        if self.ui.xAxisComboBox.currentText() == 'Order of polynomial':
            self.ui.yAxisComboBox.clear()
            yAxisList = ["Number of chunks","Overlapping"]
            self.ui.yAxisComboBox.addItems(yAxisList)
        elif self.ui.xAxisComboBox.currentText() == 'Number of chunks':
            self.ui.yAxisComboBox.clear()
            yAxisList = ["Order of polynomial","Overlapping"]
            self.ui.yAxisComboBox.addItems(yAxisList)
        elif self.ui.xAxisComboBox.currentText() == 'Overlapping':
            self.ui.yAxisComboBox.clear()
            yAxisList = ["Order of polynomial","Number of chunks"]
            self.ui.yAxisComboBox.addItems(yAxisList)  
    
    def keepConstantChunkRadioButton(self):
        if self.ui.polynomialConstantChunkRadioButton.isChecked(): self.ShowPopUpMessage("Signal curve fitting coverage may not be 100%.") 

    def FullCoverageRadioButton(self):
        if self.ui.polynomialFullCoverageRadioButton.isChecked(): self.ShowPopUpMessage("User input's number of chunks may not be kept constant.") 

    def ShowPopUpMessage(self, popUpMessage):
            messageBoxElement = QMessageBox.warning(self, 'WARING!', popUpMessage) 
    #!################################################################################
    def interpolation (self):
        self.chunckSize = ceil(1000/self.ui.polynomialNumberOfChunksSpinBox.value())
        print(self.chunckSize)
        self.order = self.ui.polynomialFittingOrderSpinBox.value()
        self.ui.mainGraphGraphicsView.clear()
        # overall point 1001 one empty 
        for i in range(0,len(self.TimeReadings)-1,self.chunckSize):
            amplitude = []
            time = []
            increment = i
            for j in range(self.chunckSize-1):
                if increment < len(self.TimeReadings):
                    amplitude.append(self.AmplitudeReadings[increment])
                    time.append(self.TimeReadings[increment])
                    increment += 1
            self.coeff = np.polyfit(time[0:int(self.chunckSize-1)], amplitude[0:int(self.chunckSize-1)],self.order)
            self.poly1d_fn = np.poly1d(self.coeff) 
            #! COODE REPETITION TACK CAAAAAAAAAAAAAAARE
            self.ui.mainGraphGraphicsView.plot(self.TimeReadings, self.AmplitudeReadings, pen=pyqtgraph.mkPen('b', width=1.5))
            self.ui.mainGraphGraphicsView.plot(time, self.poly1d_fn(time), pen=pyqtgraph.mkPen('g', width=1.5, style = QtCore.Qt.DotLine))

    def extrapolation(self):
        self.extrapolationSliderValue = self.ui.extrapolationHorizontalSlider.value()
        self.ui.extrapolationPercentageLabel.setText(f'{self.extrapolationSliderValue}% Original Signal')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())