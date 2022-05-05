from ast import increment_lineno
from math import ceil
from re import T
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import pyqtgraph
from pyqtgraph import PlotWidget
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from GUI import Ui_MainWindow
from scipy.interpolate import CubicSpline
from scipy.interpolate import make_interp_spline
from scipy.interpolate import interp1d


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
        self.ui.CurveFittingCoveragePrecentageLabel.hide()
        self.ui.CurveFittingCoveragePrecentageLcdNumber.hide()
        self.ui.signalCoveragePrecentageLabel.hide()
        self.ui.polynomialNumberOfChunksSpinBox.setValue(1)
        # Hide error map elements
        self.ui.errorMapGraphicsView.hide()
        self.ui.errorLabel.hide()
        self.ui.errorMapProgressBar.hide()
        self.polynomialShowAndHide(0)
        self.splineShowAndHide(0)
        self.cubicShowAndHide(0)
        
        # Links of GUI Elements to Methods:
        self.ui.openAction.triggered.connect(lambda: self.OpenFile())
        self.ui.polynomialMultipleChunksRadioButton.toggled.connect(lambda: self.multipleChunksRadioButton())
        self.ui.splineMultipleChunksRadioButton.toggled.connect(lambda: self.multipleChunksRadioButton())
        self.ui.cubicMultipleChunksRadioButton.toggled.connect(lambda: self.multipleChunksRadioButton())
        self.ui.polynomialOneChunkRadioButton.toggled.connect(lambda: self.oneChunkRadioButton())
        self.ui.cubicOneChunkRadioButton.toggled.connect(lambda: self.oneChunkRadioButton())
        self.ui.splineOneChunkRadioButton.toggled.connect(lambda: self.oneChunkRadioButton())
       
        self.ui.polynomialRadioButton.toggled.connect(lambda: self.interpolationMethodsRadioButton())
        self.ui.splineRadioButton.toggled.connect(lambda: self.interpolationMethodsRadioButton())
        self.ui.cubicRadioButton.toggled.connect(lambda: self.interpolationMethodsRadioButton())
        self.ui.polynomialFitPushButton.clicked.connect(lambda: self.interpolationPolynomial())
        self.ui.extrapolationHorizontalSlider.valueChanged.connect(lambda: self.extrapolation())
        self.ui.xAxisComboBox.currentIndexChanged.connect(lambda: self.xAxis())
        # self.ui.yAxisComboBox.currentIndexChanged.connect(lambda: self.yAxis())
        self.ui.polynomialOverlappingRadioButton.toggled.connect(lambda: self.OverlapRadioButton())
        self.ui.splineOverlappingRadioButton.toggled.connect(lambda: self.OverlapRadioButton())
        self.ui.cubicOverlappingRadioButton.toggled.connect(lambda: self.OverlapRadioButton())
        self.ui.polynomialNoOverlappingRadioButton.toggled.connect(lambda: self.noOverlapRadioButton())
        self.ui.cubicNoOverlappingRadioButton.toggled.connect(lambda: self.noOverlapRadioButton())
        self.ui.splineNoOverlappingRadioButton.toggled.connect(lambda: self.noOverlapRadioButton())
        self.ui.polynomialConstantChunkRadioButton.toggled.connect(lambda: self.keepConstantChunkRadioButton())
        self.ui.cubicConstantChunkRadioButton.toggled.connect(lambda: self.keepConstantChunkRadioButton())
        self.ui.splineConstantChunkRadioButton.toggled.connect(lambda: self.keepConstantChunkRadioButton())
        self.ui.polynomialFullCoverageRadioButton.toggled.connect(lambda: self.FullCoverageRadioButton())
        self.ui.cubicFullCoverageRadioButton.toggled.connect(lambda: self.FullCoverageRadioButton())
        self.ui.splineFullCoverageRadioButton.toggled.connect(lambda: self.FullCoverageRadioButton())
        self.ui.splineFitPushButton.clicked.connect(lambda: self.interpolationSpline())
        self.ui.cubicFitPushButton.clicked.connect(lambda: self.interpolationCubic())

    # Methods
    def OpenFile(self):
        self.file_name = QtWidgets.QFileDialog.getOpenFileName(caption="Choose Signal", directory="", filter="csv (*.csv)")[0]
        self.data_frame = pd.read_csv(self.file_name, encoding = 'utf-8').fillna(0)
        self.TimeReadings = self.data_frame.iloc[:,0].to_numpy()
        self.AmplitudeReadings = self.data_frame.iloc[:,1].to_numpy()
        self.ui.mainGraphGraphicsView.clear()
        self.ui.mainGraphGraphicsView.plot(self.TimeReadings, self.AmplitudeReadings, pen=pyqtgraph.mkPen('b', width=1.5))
            
    #! COODE REPETITION TACK CAAAAAAAAAAAAAAARE 
    def interpolationMethodsRadioButton(self):
        if self.ui.polynomialRadioButton.isChecked():
            self.ui.polynomialMultipleChunksRadioButton.show()
            self.ui.polynomialFitPushButton.show()
            self.ui.polynomialFittingOrderLabel.show()
            self.ui.polynomialFittingOrderSpinBox.show()
            self.ui.CurveFittingCoveragePrecentageLabel.show()
            self.ui.CurveFittingCoveragePrecentageLcdNumber.show()
            self.ui.signalCoveragePrecentageLabel.show()
            self.splineShowAndHide(0)
            self.cubicShowAndHide(0)
        elif self.ui.splineRadioButton.isChecked():
            self.ui.splineFitPushButton.show()
            self.ui.splineMultipleChunksRadioButton.show()
            self.ui.splineOneChunkRadioButton.show()
            self.ui.CurveFittingCoveragePrecentageLabel.show()
            self.ui.CurveFittingCoveragePrecentageLcdNumber.show()
            self.ui.splineFittingOrderLabel.show()
            self.ui.splineFittingOrderSpinBox.show()
            self.ui.signalCoveragePrecentageLabel.show()
            self.polynomialShowAndHide(0)
            self.cubicShowAndHide(0)
        elif self.ui.cubicRadioButton.isChecked():
            self.ui.cubicFitPushButton.show()
            self.ui.cubicMultipleChunksRadioButton.show()
            self.ui.cubicOneChunkRadioButton.show()
            self.ui.CurveFittingCoveragePrecentageLabel.show()
            self.ui.CurveFittingCoveragePrecentageLcdNumber.show()
            self.ui.signalCoveragePrecentageLabel.show()
            self.splineShowAndHide(0)
            self.polynomialShowAndHide(0)
            
    def multipleChunksRadioButton (self):
        if self.ui.polynomialMultipleChunksRadioButton.isChecked():
            self.ui.polynomialOneChunkRadioButton.show()
            self.ui.polynomialNumberOfChunksLabel.show()
            self.ui.polynomialNumberOfChunksSpinBox.show()
            self.ui.polynomialOverlappingRadioButton.show()
        elif self.ui.cubicMultipleChunksRadioButton.isChecked():
            self.ui.cubicOneChunkRadioButton.show()
            self.ui.cubicNumberOfChunksLabel.show()
            self.ui.cubicNumberOfChunksSpinBox.show()
            self.ui.cubicOverlappingRadioButton.show()
        elif self.ui.splineMultipleChunksRadioButton.isChecked():
            self.ui.splineOneChunkRadioButton.show()
            self.ui.splineNumberOfChunksLabel.show()
            self.ui.splineNumberOfChunksSpinBox.show()
            self.ui.splineOverlappingRadioButton.show()
   
    def oneChunkRadioButton (self):
        if self.ui.polynomialOneChunkRadioButton.isChecked():
            self.ui.polynomialNumberOfChunksLabel.hide()
            self.ui.polynomialNumberOfChunksSpinBox.hide()
            self.ui.polynomialOverlapSpinBox.hide()
            self.ui.polynomialOverlapLabel.hide()
            self.ui.polynomialNoOverlappingRadioButton.hide()
            self.ui.polynomialOverlappingRadioButton.hide()
            self.ui.polynomialOverlapSpinBox.hide()
            self.ui.polynomialOverlapLabel.hide()
            self.ui.polynomialFullCoverageRadioButton.hide()
            self.ui.polynomialConstantChunkRadioButton.hide()
        elif self.ui.splineOneChunkRadioButton.isChecked():
            self.ui.splineNumberOfChunksLabel.hide()
            self.ui.splineNumberOfChunksSpinBox.hide()
            self.ui.splineOverlapSpinBox.hide()
            self.ui.splineOverlapLabel.hide()
            self.ui.splineNoOverlappingRadioButton.hide()
            self.ui.splineOverlappingRadioButton.hide()
            self.ui.splineOverlapSpinBox.hide()
            self.ui.splineOverlapLabel.hide()
            self.ui.splineFullCoverageRadioButton.hide()
            self.ui.splineConstantChunkRadioButton.hide()
        elif self.ui.cubicOneChunkRadioButton.isChecked():
            self.ui.cubicNumberOfChunksLabel.hide()
            self.ui.cubicNumberOfChunksSpinBox.hide()
            self.ui.cubicOverlapSpinBox.hide()
            self.ui.cubicOverlapLabel.hide()
            self.ui.cubicNoOverlappingRadioButton.hide()
            self.ui.cubicOverlappingRadioButton.hide()
            self.ui.cubicOverlapSpinBox.hide()
            self.ui.cubicOverlapLabel.hide()
            self.ui.cubicFullCoverageRadioButton.hide()
            self.ui.cubicConstantChunkRadioButton.hide()

    def OverlapRadioButton(self):
        if self.ui.polynomialOverlappingRadioButton.isChecked():
            self.ui.polynomialOverlapSpinBox.show()
            self.ui.polynomialOverlapLabel.show()
            self.ui.polynomialFullCoverageRadioButton.show()
            self.ui.polynomialConstantChunkRadioButton.show()
            self.ui.polynomialNoOverlappingRadioButton.show()
        elif self.ui.cubicOverlappingRadioButton.isChecked():
            self.ui.cubicOverlapSpinBox.show()
            self.ui.cubicOverlapLabel.show()
            self.ui.cubicFullCoverageRadioButton.show()
            self.ui.cubicConstantChunkRadioButton.show()
            self.ui.cubicNoOverlappingRadioButton.show()
        elif self.ui.splineOverlappingRadioButton.isChecked():
            self.ui.splineOverlapSpinBox.show()
            self.ui.splineOverlapLabel.show()
            self.ui.splineFullCoverageRadioButton.show()
            self.ui.splineConstantChunkRadioButton.show()
            self.ui.splineNoOverlappingRadioButton.show()

    def noOverlapRadioButton(self):
        if self.ui.polynomialNoOverlappingRadioButton.isChecked():
            self.ui.polynomialOverlapSpinBox.hide()
            self.ui.polynomialOverlapLabel.hide()
            self.ui.polynomialFullCoverageRadioButton.hide()
            self.ui.polynomialConstantChunkRadioButton.hide()
        elif self.ui.cubicNoOverlappingRadioButton.isChecked():
            self.ui.cubicOverlapSpinBox.hide()
            self.ui.cubicOverlapLabel.hide()
            self.ui.cubicFullCoverageRadioButton.hide()
            self.ui.cubicConstantChunkRadioButton.hide()
        elif self.ui.splineNoOverlappingRadioButton.isChecked():
            self.ui.splineOverlapSpinBox.hide()
            self.ui.splineOverlapLabel.hide()
            self.ui.splineFullCoverageRadioButton.hide()
            self.ui.splineConstantChunkRadioButton.hide()

    def polynomialShowAndHide(self, show):
        if show == 0: #hide
            self.ui.polynomialOneChunkRadioButton.hide()
            self.ui.polynomialMultipleChunksRadioButton.hide()
            self.ui.polynomialFitPushButton.hide()
            self.ui.polynomialFittingOrderLabel.hide()
            self.ui.polynomialFittingOrderSpinBox.hide()
            self.ui.polynomialNumberOfChunksLabel.hide()
            self.ui.polynomialNumberOfChunksSpinBox.hide()
            self.ui.polynomialOverlapSpinBox.hide()
            self.ui.polynomialOverlapLabel.hide()
            self.ui.polynomialNumberOfChunksLabel.hide()
            self.ui.polynomialNumberOfChunksSpinBox.hide()
            self.ui.polynomialOverlapSpinBox.hide()
            self.ui.polynomialOverlapLabel.hide()
            self.ui.polynomialNoOverlappingRadioButton.hide()
            self.ui.polynomialOverlappingRadioButton.hide()
            self.ui.polynomialOverlapSpinBox.hide()
            self.ui.polynomialOverlapLabel.hide()
            self.ui.polynomialFullCoverageRadioButton.hide()
            self.ui.polynomialConstantChunkRadioButton.hide()
        elif show == 1: #show
            self.ui.polynomialOneChunkRadioButton.show()
            self.ui.polynomialMultipleChunksRadioButton.show()
            self.ui.polynomialFitPushButton.show()
            self.ui.polynomialFittingOrderLabel.show()
            self.ui.polynomialFittingOrderSpinBox.show()
            self.ui.polynomialNumberOfChunksLabel.show()
            self.ui.polynomialNumberOfChunksSpinBox.show()
            self.ui.polynomialOverlapSpinBox.show()
            self.ui.polynomialOverlapLabel.show()
            self.ui.polynomialCurveFittingCoveragePrecentageLabel.show()
            self.ui.polynomialCurveFittingCoveragePrecentageLcdNumber.show()
            self.ui.polynomialNumberOfChunksLabel.show()
            self.ui.polynomialNumberOfChunksSpinBox.show()
            self.ui.polynomialOverlapSpinBox.show()
            self.ui.polynomialOverlapLabel.show()
            self.ui.polynomialNoOverlappingRadioButton.show()
            self.ui.polynomialOverlappingRadioButton.show()
            self.ui.polynomialOverlapSpinBox.show()
            self.ui.polynomialOverlapLabel.show()
            self.ui.polynomialFullCoverageRadioButton.show()
            self.ui.polynomialConstantChunkRadioButton.show()
    
    def splineShowAndHide(self, show):
        if show == 0: #hide
            self.ui.splineFitPushButton.hide()
            self.ui.splineConstantChunkRadioButton.hide()
            self.ui.splineFullCoverageRadioButton.hide()
            self.ui.splineMultipleChunksRadioButton.hide()
            self.ui.splineNoOverlappingRadioButton.hide()
            self.ui.splineNumberOfChunksLabel.hide()
            self.ui.splineNumberOfChunksSpinBox.hide()
            self.ui.splineOneChunkRadioButton.hide()
            self.ui.splineOverlapLabel.hide()
            self.ui.splineOverlappingRadioButton.hide()
            self.ui.splineOverlapSpinBox.hide()
            self.ui.splineFittingOrderLabel.hide()
            self.ui.splineFittingOrderSpinBox.hide()
        elif show == 1: #show
            self.ui.splineFitPushButton.show()
            self.ui.splineConstantChunkRadioButton.show()
            self.ui.splineFullCoverageRadioButton.show()
            self.ui.splineMultipleChunksRadioButton.show()
            self.ui.splineNoOverlappingRadioButton.show()
            self.ui.splineNumberOfChunksLabel.show()
            self.ui.splineNumberOfChunksSpinBox.show()
            self.ui.splineOneChunkRadioButton.show()
            self.ui.splineOverlapLabel.show()
            self.ui.splineOverlappingRadioButton.show()
            self.ui.splineOverlapSpinBox.show()
            self.ui.splineFittingOrderLabel.show()
            self.ui.splineFittingOrderSpinBox.show()

    def cubicShowAndHide(self, show):
        if show == 0: #hide
            self.ui.cubicConstantChunkRadioButton.hide()
            self.ui.cubicFullCoverageRadioButton.hide()
            self.ui.cubicMultipleChunksRadioButton.hide()
            self.ui.cubicNoOverlappingRadioButton.hide()
            self.ui.cubicNumberOfChunksLabel.hide()
            self.ui.cubicNumberOfChunksSpinBox.hide()
            self.ui.cubicOneChunkRadioButton.hide()
            self.ui.cubicOverlapLabel.hide()
            self.ui.cubicOverlappingRadioButton.hide()
            self.ui.cubicOverlapSpinBox.hide()
            self.ui.cubicFitPushButton.hide()
        elif show == 1: #show
            self.ui.cubicFitPushButton.show()
            self.ui.cubicConstantChunkRadioButton.show()
            self.ui.cubicFullCoverageRadioButton.show()
            self.ui.cubicMultipleChunksRadioButton.show()
            self.ui.cubicNoOverlappingRadioButton.show()
            self.ui.cubicNumberOfChunksLabel.show()
            self.ui.cubicNumberOfChunksSpinBox.show()
            self.ui.cubicOneChunkRadioButton.show()
            self.ui.cubicOverlapLabel.show()
            self.ui.cubicOverlappingRadioButton.show()
            self.ui.cubicOverlapSpinBox.show()

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

    # def yAxis(self):
    #     if self.ui.yAxisComboBox.currentText() == 'Order of polynomial':
    #         self.ui.xAxisComboBox.clear()
    #         xAxisList = ["Number of chunks","Overlapping"]
    #         self.ui.xAxisComboBox.addItems(xAxisList)
    #     elif self.ui.yAxisComboBox.currentText() == 'Number of chunks':
    #         self.ui.xAxisComboBox.clear()
    #         xAxisList = ["Order of polynomial","Overlapping"]
    #         self.ui.xAxisComboBox.addItems(xAxisList)
    #     elif self.ui.yAxisComboBox.currentText() == 'Overlapping':
    #         self.ui.xAxisComboBox.clear()
    #         xAxisList = ["Order of polynomial","Number of chunks"]
    #         self.ui.xAxisComboBox.addItems(xAxisList) 
        
    
    def keepConstantChunkRadioButton(self):
        if self.ui.polynomialConstantChunkRadioButton.isChecked(): self.ShowPopUpMessage("Signal curve fitting coverage may not be 100%.") 
        elif self.ui.cubicConstantChunkRadioButton.isChecked(): self.ShowPopUpMessage("Signal curve fitting coverage may not be 100%.") 
        elif self.ui.splineConstantChunkRadioButton.isChecked(): self.ShowPopUpMessage("Signal curve fitting coverage may not be 100%.") 

    def FullCoverageRadioButton(self):
        if self.ui.polynomialFullCoverageRadioButton.isChecked(): self.ShowPopUpMessage("User input's number of chunks may not be kept constant.") 
        elif self.ui.cubicFullCoverageRadioButton.isChecked(): self.ShowPopUpMessage("User input's number of chunks may not be kept constant.") 
        elif self.ui.splineFullCoverageRadioButton.isChecked(): self.ShowPopUpMessage("User input's number of chunks may not be kept constant.") 

    def ShowPopUpMessage(self, popUpMessage):
            messageBoxElement = QMessageBox.warning(self, 'WARING!', popUpMessage) 
    #!################################################################################
    def interpolationPolynomial (self):
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

    def clearErrorMap(self):
        self.figure = plt.figure(figsize=(15,5))
        self.Canvas = FigureCanvas(self.figure)
        self.ui.errorMapGridLayout.addWidget(self.Canvas,0, 0, 1, 1)

    def interpolationSpline(self):
        self.chunkSizespline = int(1000/self.ui.splineNumberOfChunksSpinBox.value())
        order = self.ui.splineFittingOrderSpinBox.value()
        self.ui.mainGraphGraphicsView.clear()
        # tnew = np.linspace(min(self.TimeReadings), max(self.TimeReadings),1000)
        # spline = make_interp_spline(self.TimeReadings, self.AmplitudeReadings, k=1)
        # ampNew = spline(tnew)
        # self.ui.mainGraphGraphicsView.plot(self.TimeReadings, self.AmplitudeReadings, pen=pyqtgraph.mkPen('b', width=1.5))
        # self.ui.mainGraphGraphicsView.plot(tnew, ampNew, pen=pyqtgraph.mkPen('g', width=1.5, style = QtCore.Qt.DotLine))
        self.ui.mainGraphGraphicsView.plot(self.TimeReadings, self.AmplitudeReadings, pen=pyqtgraph.mkPen('b', width=1.5))
        
        for i in range(0,len(self.TimeReadings)-1,self.chunkSizespline):
            amplitude = []
            time = []
            increment = i
            for j in range(self.chunkSizespline-1):
                if increment < len(self.TimeReadings):
                    amplitude.append(self.AmplitudeReadings[increment])
                    time.append(self.TimeReadings[increment])
                    increment += 1
            # tmodel = np.linspace(min(time), max(time), 1000)
            tnew = np.linspace(min(time), max(time),1000)
            spline = make_interp_spline(time[0:int(self.chunkSizespline-1)], amplitude[0:int(self.chunkSizespline-1)], k=order)
            ampNew = spline(tnew)
            # cs = CubicSpline(time[0:int(self.chunkSizespline-1)], amplitude[0:int(self.chunkSizespline-1)], bc_type='clamped')
            # self.ui.mainGraphGraphicsView.plot(self.TimeReadings, self.AmplitudeReadings, pen=pyqtgraph.mkPen('b', width=1.5))
            # self.ui.mainGraphGraphicsView.plot(tmodel, cs(tmodel), pen=pyqtgraph.mkPen('g', width=1.5, style = QtCore.Qt.DotLine))
            self.ui.mainGraphGraphicsView.plot(tnew, ampNew, pen=pyqtgraph.mkPen('g', width=1.5, style = QtCore.Qt.DotLine))

    def interpolationCubic(self):
        tnew = np.linspace(min(self.TimeReadings), max(self.TimeReadings),1000)
        cubic = interp1d(self.TimeReadings, self.AmplitudeReadings, kind='cubic')
        self.ui.mainGraphGraphicsView.plot(self.TimeReadings, self.AmplitudeReadings, pen=pyqtgraph.mkPen('b', width=1.5))
        self.ui.mainGraphGraphicsView.plot(tnew, cubic(tnew), pen=pyqtgraph.mkPen('g', width=1.5, style = QtCore.Qt.DotLine))


    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())