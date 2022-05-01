from ast import increment_lineno
from math import ceil
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
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

        self.ui.cubicSplineFittingOrderLabel.hide()
        self.ui.cubicSplineFittingOrderSpinBox.hide()
        
        # Links of GUI Elements to Methods:
        self.ui.openAction.triggered.connect(lambda: self.OpenFile())
        self.ui.polynomialMultipleChunksRadioButton.toggled.connect(lambda: self.radioButtonMultiple())
        self.ui.polynomialOneChunkRadioButton.toggled.connect(lambda: self.radioButton())
        self.ui.polynomialRadioButton.toggled.connect(lambda: self.polynomial())
        self.ui.cubicSplineRadioButton.toggled.connect(lambda: self.cubicSpline())
        self.ui.bicubicRadioButton.toggled.connect(lambda: self.bicubic())
        self.ui.polynomialFitPushButton.clicked.connect(lambda: self.interpolation())

    # Methods
    def OpenFile(self):
        self.file_name = QtWidgets.QFileDialog.getOpenFileName(caption="Choose Signal", directory="", filter="csv (*.csv)")[0]
        self.data_frame = pd.read_csv(self.file_name, encoding = 'utf-8').fillna(0)
        self.TimeReadings = self.data_frame.iloc[:,0].to_numpy()
        self.AmplitudeReadings = self.data_frame.iloc[:,1].to_numpy()
        self.ui.mainGraphGraphicsView.plot(self.TimeReadings, self.AmplitudeReadings, pen=pyqtgraph.mkPen('b', width=1.5))
            
    #! COODE REPETITION TACK CAAAAAAAAAAAAAAARE        
    def radioButtonMultiple (self):
        if self.ui.polynomialMultipleChunksRadioButton.isChecked():
            self.ui.polynomialNumberOfChunksLabel.show()
            self.ui.polynomialNumberOfChunksSpinBox.show()
            self.ui.polynomialOerlapSpinBox.show()
            self.ui.polynomialOverlapLabel.show()


    def radioButton (self):
        if self.ui.polynomialOneChunkRadioButton.isChecked():
            self.oneChunck = 1
            self.ui.polynomialNumberOfChunksLabel.hide()
            self.ui.polynomialNumberOfChunksSpinBox.hide()
            self.ui.polynomialOerlapSpinBox.hide()
            self.ui.polynomialOverlapLabel.hide()

    def polynomial(self):
        if self.ui.polynomialRadioButton.isChecked():
            self.ui.polynomialOneChunkRadioButton.show()
            self.ui.polynomialMultipleChunksRadioButton.show()
            self.ui.polynomialFitPushButton.show()
            self.ui.polynomialFittingOrderLabel.show()
            self.ui.polynomialFittingOrderSpinBox.show()

            self.ui.cubicSplineFittingOrderLabel.hide()
            self.ui.cubicSplineFittingOrderSpinBox.hide()
    
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
################################################################################
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

    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())