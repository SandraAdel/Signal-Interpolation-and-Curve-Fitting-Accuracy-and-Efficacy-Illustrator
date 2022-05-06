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
from GUI2 import Ui_MainWindow
from scipy.interpolate import CubicSpline
from scipy.interpolate import make_interp_spline
from scipy.interpolate import interp1d
import seaborn as sns
from sklearn.metrics import mean_squared_error
from PyQt5.QtWidgets import QWidget, QApplication, QProgressBar, QMainWindow, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot, QRunnable, QThreadPool
import time
from matplotlib.figure import Figure
import matplotlib.image as mpimg
from sympy import S, symbols, printing
from PyQt5.QtGui import QIcon, QPixmap
from io import BytesIO


# Sandra's Addition: Threading related
class WorkerSignals(QObject):
    started = pyqtSignal()
    finished = pyqtSignal()
    progress = pyqtSignal(int)

class Worker(QRunnable):

    signals = WorkerSignals()

    def __init__(self, window_object, x_axis_parameter, y_axis_parameter, constant_parameter_value):
        super().__init__()
        self.is_paused = False
        self.is_stopped = False
        self.window_object = window_object
        self.errors_matrix = None
        self.x_axis_parameter_dictionary, self.y_axis_parameter_dictionary = None, None
        self.curve_fitting_parameters_list = [ {'Parameter Name': 'Number of Chunks', 'Start Range': 1, 'End Range': 20, 'Full Range': 20}, {'Parameter Name': 'Overlapping Percentage', 'Start Range': 0, 'End Range': 25, 'Full Range':26}, {'Parameter Name': 'Polynomial Order', 'Start Range': 0, 'End Range': 10, 'Full Range': 11} ]
        self.x_axis_parameter, self.y_axis_parameter, self.constant_parameter_value = x_axis_parameter, y_axis_parameter, constant_parameter_value

    def AssignLoopingRangeForCurveFittingParameters(self, dictionary_of_curve_fitting_parameter_to_assign, x_axis_parameter, y_axis_parameter, constant_parameter_value):
        if x_axis_parameter == dictionary_of_curve_fitting_parameter_to_assign['Parameter Name'] or y_axis_parameter == dictionary_of_curve_fitting_parameter_to_assign['Parameter Name']:
            return (dictionary_of_curve_fitting_parameter_to_assign['Start Range'], dictionary_of_curve_fitting_parameter_to_assign['End Range'])
        else:
            return (constant_parameter_value, constant_parameter_value)

    @pyqtSlot()
    def run(self):
        self.signals.started.emit()

        current_progress = 0
        self.x_axis_parameter_dictionary = GetDictionaryByKeyValuePair(self.curve_fitting_parameters_list, 'Parameter Name', self.x_axis_parameter)
        self.y_axis_parameter_dictionary = GetDictionaryByKeyValuePair(self.curve_fitting_parameters_list, 'Parameter Name', self.y_axis_parameter)
        number_of_chunks_range_on_error_map = self.AssignLoopingRangeForCurveFittingParameters( GetDictionaryByKeyValuePair(self.curve_fitting_parameters_list, 'Parameter Name', 'Number of Chunks'), self.x_axis_parameter, self.y_axis_parameter, self.constant_parameter_value )
        overlapping_percentage_range_on_error_map = self.AssignLoopingRangeForCurveFittingParameters( GetDictionaryByKeyValuePair(self.curve_fitting_parameters_list, 'Parameter Name', 'Overlapping Percentage'), self.x_axis_parameter, self.y_axis_parameter, self.constant_parameter_value )
        polynomial_order_range_on_error_map = self.AssignLoopingRangeForCurveFittingParameters( GetDictionaryByKeyValuePair(self.curve_fitting_parameters_list, 'Parameter Name', 'Polynomial Order'), self.x_axis_parameter, self.y_axis_parameter, self.constant_parameter_value )
        self.errors_matrix = np.zeros(( self.y_axis_parameter_dictionary['Full Range'] , self.x_axis_parameter_dictionary['Full Range'] ))
        progress_step = 100/(self.errors_matrix.size)
        row_index = self.y_axis_parameter_dictionary['Full Range'] - 1
        column_index = 0
        for overlapping_percentage in range(overlapping_percentage_range_on_error_map[0], overlapping_percentage_range_on_error_map[1]+1):
            for polynomial_order in range(polynomial_order_range_on_error_map[0], polynomial_order_range_on_error_map[1]+1):
                for number_of_chunks in range(number_of_chunks_range_on_error_map[0], number_of_chunks_range_on_error_map[1]+1):
                    __ , MSE_error = self.window_object.CurveFitFunctionality(number_of_chunks, overlapping_percentage, 'Polynomial', polynomial_order, False)
                    self.errors_matrix[ row_index, column_index ] = MSE_error
                    current_progress += progress_step
    
                    self.signals.progress.emit(round(current_progress))
                    # FOR PAUSING
                    # REMOVE LATER
                    #time.sleep(0.05)                   
                    while self.is_paused:
                        time.sleep(0)
                    if self.is_stopped:
                        return

                    if self.x_axis_parameter == 'Number of Chunks':
                        column_index += 1
                    elif self.y_axis_parameter == 'Number of Chunks':
                        row_index -= 1
                if self.x_axis_parameter == 'Number of Chunks':
                    column_index = 0
                    row_index -= 1
                elif self.y_axis_parameter == 'Number of Chunks':
                    column_index += 1
                    row_index = self.y_axis_parameter_dictionary['Full Range'] - 1
                if self.x_axis_parameter == 'Polynomial Order' and self.y_axis_parameter != 'Number of Chunks':
                    column_index += 1
                elif self.y_axis_parameter == 'Polynomial Order'and self.x_axis_parameter != 'Number of Chunks':
                    row_index -= 1
            if self.x_axis_parameter == 'Polynomial Order':
                column_index = 0
                row_index -= 1
            elif self.y_axis_parameter == 'Polynomial Order':
                column_index += 1
                row_index = self.y_axis_parameter_dictionary['Full Range'] - 1
        self.signals.finished.emit()

    def pause_and_resume(self, order):
        if order == 'Pause':
            self.is_paused = True
        elif order == 'Resume':
            self.is_paused = False

    def stop(self):
        self.is_stopped = True

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
        self.isMultiple = False
        self.chunkNumber = 1
        self.ui.CurveFittingCoveragePrecentageLabel.hide()
        self.ui.CurveFittingCoveragePrecentageLcdNumber.hide()
        self.ui.signalCoveragePrecentageLabel.hide()
        self.ui.polynomialNumberOfChunksSpinBox.setValue(1)
        # Hide error map elements
        self.ui.errorMapGraphicsView.hide()
        # self.ui.errorLabel.hide()
        self.ui.errorMapProgressBar.hide()
        self.polynomialShowAndHide(0)
        self.splineShowAndHide(0)
        self.cubicShowAndHide(0)
        # Sandra's Addition
        self.number_of_readings  = 1000
        self.prioritizing_constant_number_of_chunks_over_signal_interpolation_coverage = False
        self.signal_curve_fitting_coverage = None
        self.threadRunning = False
        self.threadPaused = False
        self.ui.pauseAndRezoomErrorMapPushButton.setEnabled(False)
        self.threadpool = QThreadPool()
        self.ui.startAndCancelErrorMapPushButton.pressed.connect(self.startThreadRunner)
        self.ui.pauseAndRezoomErrorMapPushButton.pressed.connect(self.pauseAndResumeHandler)
        self.error_map_x_axis_parameter = None
        self.error_map_y_axis_parameter = None
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
        self.ui.polynomialFitPushButton.clicked.connect(lambda: self.interpolationMethods())
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
        self.ui.polynomialFittingOrderSpinBox.valueChanged.connect(lambda: self.equation())
        self.ui.extrapolationHorizontalSlider.valueChanged.connect(lambda: self.equation())
        self.ui.latexEquationComboBox.currentIndexChanged.connect(lambda: self.equation())



    # Methods
    def OpenFile(self):
        self.file_name = QtWidgets.QFileDialog.getOpenFileName(caption="Choose Signal", directory="", filter="csv (*.csv)")[0]
        self.data_frame = pd.read_csv(self.file_name, encoding = 'utf-8').fillna(0)
        self.TimeReadings = self.data_frame.iloc[:,0].to_numpy()
        self.AmplitudeReadings = self.data_frame.iloc[:,1].to_numpy()
        self.ui.mainGraphGraphicsView.clear()
        self.ui.mainGraphGraphicsView.setYRange(min(self.AmplitudeReadings), max(self.AmplitudeReadings))
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
            self.setSpinBox('Polynomial', False)
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
            self.setSpinBox('Spline', False)
        elif self.ui.cubicRadioButton.isChecked():
            self.ui.cubicFitPushButton.show()
            self.ui.cubicMultipleChunksRadioButton.show()
            self.ui.cubicOneChunkRadioButton.show()
            self.ui.CurveFittingCoveragePrecentageLabel.show()
            self.ui.CurveFittingCoveragePrecentageLcdNumber.show()
            self.ui.signalCoveragePrecentageLabel.show()
            self.splineShowAndHide(0)
            self.polynomialShowAndHide(0)
            self.setSpinBox('Cubic', True)

            
    def multipleChunksRadioButton (self):
        if self.ui.polynomialMultipleChunksRadioButton.isChecked():
            self.isMultiple = True
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
            self.isMultiple = False
            self.setSpinBox('Polynomial', True)
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
            self.setSpinBox('Spline', True)
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
            self.setSpinBox('Cubic', True)
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
        if self.ui.xAxisComboBox.currentText() == 'Polynomial Order':
            self.ui.yAxisComboBox.clear()
            yAxisList = ["Number of Chunks","Overlapping Percentage"]
            self.ui.yAxisComboBox.addItems(yAxisList)
        elif self.ui.xAxisComboBox.currentText() == 'Number of Chunks':
            self.ui.yAxisComboBox.clear()
            yAxisList = ["Polynomial Order","Overlapping Percentage"]
            self.ui.yAxisComboBox.addItems(yAxisList)
        elif self.ui.xAxisComboBox.currentText() == 'Overlapping Percentage':
            self.ui.yAxisComboBox.clear()
            yAxisList = ["Polynomial Order","Number of Chunks"]
            self.ui.yAxisComboBox.addItems(yAxisList) 

    # def yAxis(self):
    #     if self.ui.yAxisComboBox.currentText() == 'Polynomial Order':
    #         self.ui.xAxisComboBox.clear()
    #         xAxisList = ["Number of Chunks","Overlapping Percentage"]
    #         self.ui.xAxisComboBox.addItems(xAxisList)
    #     elif self.ui.yAxisComboBox.currentText() == 'Number of Chunks':
    #         self.ui.xAxisComboBox.clear()
    #         xAxisList = ["Polynomial Order","Overlapping Percentage"]
    #         self.ui.xAxisComboBox.addItems(xAxisList)
    #     elif self.ui.yAxisComboBox.currentText() == 'Overlapping Percentage':
    #         self.ui.xAxisComboBox.clear()
    #         xAxisList = ["Polynomial Order","Number of Chunks"]
    #         self.ui.xAxisComboBox.addItems(xAxisList) 
        
    
    def keepConstantChunkRadioButton(self):
        if self.ui.polynomialConstantChunkRadioButton.isChecked(): 
            self.ShowPopUpMessage("Signal curve fitting coverage may not be 100%.") 
            self.prioritizing_constant_number_of_chunks_over_signal_interpolation_coverage = True
        elif self.ui.cubicConstantChunkRadioButton.isChecked(): 
            self.ShowPopUpMessage("Signal curve fitting coverage may not be 100%.")
            self.prioritizing_constant_number_of_chunks_over_signal_interpolation_coverage = True 
        elif self.ui.splineConstantChunkRadioButton.isChecked(): 
            self.ShowPopUpMessage("Signal curve fitting coverage may not be 100%.")
            self.prioritizing_constant_number_of_chunks_over_signal_interpolation_coverage = True 

    def FullCoverageRadioButton(self):
        if self.ui.polynomialFullCoverageRadioButton.isChecked(): 
            self.ShowPopUpMessage("User input's number of chunks may not be kept constant.")
            self.prioritizing_constant_number_of_chunks_over_signal_interpolation_coverage = False 
        elif self.ui.cubicFullCoverageRadioButton.isChecked(): 
            self.ShowPopUpMessage("User input's number of chunks may not be kept constant.")
            self.prioritizing_constant_number_of_chunks_over_signal_interpolation_coverage = False 
        elif self.ui.splineFullCoverageRadioButton.isChecked(): 
            self.ShowPopUpMessage("User input's number of chunks may not be kept constant.") 
            self.prioritizing_constant_number_of_chunks_over_signal_interpolation_coverage = False

    def ShowPopUpMessage(self, popUpMessage):
            messageBoxElement = QMessageBox.warning(self, 'WARING!', popUpMessage) 
    
    def setSpinBox(self, kind, one):
        if kind == 'Polynomial'and one == True:
            self.ui.splineFittingOrderSpinBox.setValue(0)
            self.ui.splineNumberOfChunksSpinBox.setValue(1)
            self.ui.splineOverlapSpinBox.setValue(0)
            self.ui.cubicNumberOfChunksSpinBox.setValue(1)
            self.ui.cubicOverlapSpinBox.setValue(0)
            self.ui.polynomialOverlapSpinBox.setValue(0)
            self.ui.polynomialNumberOfChunksSpinBox.setValue(1)
        elif kind == 'Polynomial'and one == False:
            self.ui.splineFittingOrderSpinBox.setValue(0)
            self.ui.splineNumberOfChunksSpinBox.setValue(1)
            self.ui.splineOverlapSpinBox.setValue(0)
            self.ui.cubicNumberOfChunksSpinBox.setValue(1)
            self.ui.cubicOverlapSpinBox.setValue(0)
            self.ui.polynomialOverlapSpinBox.setValue(0)
            self.ui.polynomialNumberOfChunksSpinBox.setValue(1)
            self.ui.polynomialFittingOrderSpinBox.setValue(0)
        elif kind == 'Spline'and one == True:
            self.ui.cubicNumberOfChunksSpinBox.setValue(1)
            self.ui.cubicOverlapSpinBox.setValue(0)
            self.ui.polynomialOverlapSpinBox.setValue(0)
            self.ui.polynomialNumberOfChunksSpinBox.setValue(1)
            self.ui.polynomialFittingOrderSpinBox.setValue(0)
            self.ui.splineOverlapSpinBox.setValue(0)
            self.ui.splineNumberOfChunksSpinBox.setValue(1)
        elif kind == 'Spline'and one == False:
            self.ui.cubicNumberOfChunksSpinBox.setValue(1)
            self.ui.cubicOverlapSpinBox.setValue(0)
            self.ui.polynomialOverlapSpinBox.setValue(0)
            self.ui.polynomialNumberOfChunksSpinBox.setValue(1)
            self.ui.polynomialFittingOrderSpinBox.setValue(0)
            self.ui.splineOverlapSpinBox.setValue(0)
            self.ui.splineNumberOfChunksSpinBox.setValue(1)
            self.ui.splineFittingOrderSpinBox.setValue(0)
        elif kind == 'Cubic' and one == True:            
            self.ui.cubicNumberOfChunksSpinBox.setValue(1)
            self.ui.cubicOverlapSpinBox.setValue(0)
            self.ui.polynomialOverlapSpinBox.setValue(0)
            self.ui.polynomialNumberOfChunksSpinBox.setValue(1)
            self.ui.polynomialFittingOrderSpinBox.setValue(0)
            self.ui.splineOverlapSpinBox.setValue(0)
            self.ui.splineNumberOfChunksSpinBox.setValue(1)
            self.ui.splineFittingOrderSpinBox.setValue(0)


    #!################################################################################
    def interpolationPolynomial (self):
        self.chunckSize = ceil(1000/self.ui.polynomialNumberOfChunksSpinBox.value())
        # print(self.chunckSize)
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
        interpolated_curve_readings, curve_fitting_MSE = self.CurveFitFunctionality(self.ui.polynomialNumberOfChunksSpinBox.value(),self.ui.polynomialOverlapSpinBox.value(),'Polynomial',self.order,True)
        print(interpolated_curve_readings)
        print(curve_fitting_MSE)

    def extrapolation(self):
        self.extrapolationSliderValue = self.ui.extrapolationHorizontalSlider.value()
        self.ui.extrapolationPercentageLabel.setText(f'{self.extrapolationSliderValue}% Original Signal')
        self.lastIndex= int((self.extrapolationSliderValue/100)* len(self.TimeReadings))
        self.order = self.ui.polynomialFittingOrderSpinBox.value()
        amplitude = []
        time = []
        residualTime= []
        extrapolatedAmplitude= []
        time = self.TimeReadings[0:self.lastIndex]
        amplitude = self.AmplitudeReadings[0:self.lastIndex] 
        residualTime= self.TimeReadings[self.lastIndex:len(self.TimeReadings)]        
        self.coeff = np.polyfit(time, amplitude,self.order)
        self.poly1d_fn = np.poly1d(self.coeff) 
        extrapolatedAmplitude= np.polyval(self.coeff, residualTime) 
        # print(residualTime)
        # print(extrapolatedAmplitude)
        self.ui.mainGraphGraphicsView.clear()
        self.ui.mainGraphGraphicsView.plot(self.TimeReadings, self.AmplitudeReadings, pen=pyqtgraph.mkPen('b', width=1.5))
        self.ui.mainGraphGraphicsView.plot(time, self.poly1d_fn(time), pen=pyqtgraph.mkPen('g', width=1.5, style = QtCore.Qt.DotLine))
        self.ui.mainGraphGraphicsView.plot(residualTime, extrapolatedAmplitude, pen=pyqtgraph.mkPen('r', width=1.5, style = QtCore.Qt.DotLine))

    def clearErrorMap(self):
        self.figure = plt.figure(figsize=(15,5))
        self.axes = self.figure.get_axes()
        self.Canvas = FigureCanvas(self.figure)
        self.ui.errorMapGridLayout.addWidget(self.Canvas,0, 0, 1, 1)

    def interpolationSpline(self):
        # self.chunkSizespline = int(1000/self.ui.splineNumberOfChunksSpinBox.value())
        # order = self.ui.splineFittingOrderSpinBox.value()
        self.ui.mainGraphGraphicsView.clear()
        self.ui.mainGraphGraphicsView.plot(self.TimeReadings, self.AmplitudeReadings, pen=pyqtgraph.mkPen('b', width=1.5))
        interpolated_curve_readings, curve_fitting_MSE = self.CurveFitFunctionality(self.ui.splineNumberOfChunksSpinBox.value(),self.ui.splineOverlapSpinBox.value(),'Spline', self.ui.splineFittingOrderSpinBox.value(), True)
        self.CurveFittingCoverageCalculation(interpolated_curve_readings)
        # tnew = np.linspace(min(self.TimeReadings), max(self.TimeReadings),1000)
        # spline = make_interp_spline(self.TimeReadings, self.AmplitudeReadings, k=1)
        # ampNew = spline(tnew)
        # self.ui.mainGraphGraphicsView.plot(self.TimeReadings, self.AmplitudeReadings, pen=pyqtgraph.mkPen('b', width=1.5))
        # self.ui.mainGraphGraphicsView.plot(tnew, ampNew, pen=pyqtgraph.mkPen('g', width=1.5, style = QtCore.Qt.DotLine))
        # self.ui.mainGraphGraphicsView.plot(self.TimeReadings, self.AmplitudeReadings, pen=pyqtgraph.mkPen('b', width=1.5))
        
        # for i in range(0,len(self.TimeReadings)-1,self.chunkSizespline):
        #     amplitude = []
        #     time = []
        #     increment = i
        #     for j in range(self.chunkSizespline-1):
        #         if increment < len(self.TimeReadings):
        #             amplitude.append(self.AmplitudeReadings[increment])
        #             time.append(self.TimeReadings[increment])
        #             increment += 1
        #     tmodel = np.linspace(min(time), max(time), 1000)
        #     tnew = np.linspace(min(time), max(time),1000)
        #     spline = make_interp_spline(time[0:int(self.chunkSizespline-1)], amplitude[0:int(self.chunkSizespline-1)], k=order)
        #     ampNew = spline(tnew)
        #     print(np.poly1d(spline))
        #     cs = CubicSpline(time[0:int(self.chunkSizespline-1)], amplitude[0:int(self.chunkSizespline-1)], bc_type='clamped')
        #     self.ui.mainGraphGraphicsView.plot(self.TimeReadings, self.AmplitudeReadings, pen=pyqtgraph.mkPen('b', width=1.5))
        #     self.ui.mainGraphGraphicsView.plot(tmodel, cs(tmodel), pen=pyqtgraph.mkPen('g', width=1.5, style = QtCore.Qt.DotLine))
        #     self.ui.mainGraphGraphicsView.plot(tnew, ampNew, pen=pyqtgraph.mkPen('g', width=1.5, style = QtCore.Qt.DotLine))

    def interpolationCubic(self):
        # tnew = np.linspace(min(self.TimeReadings), max(self.TimeReadings),1000)
        self.ui.mainGraphGraphicsView.clear()
        self.ui.mainGraphGraphicsView.plot(self.TimeReadings, self.AmplitudeReadings, pen=pyqtgraph.mkPen('b', width=1.5))
        interpolated_curve_readings, curve_fitting_MSE = self.CurveFitFunctionality(self.ui.cubicNumberOfChunksSpinBox.value(),self.ui.cubicOverlapSpinBox.value(),'Cubic', 'cubic', True)
        self.CurveFittingCoverageCalculation(interpolated_curve_readings)
        # self.chunkSizespline = int(1000/self.ui.cubicNumberOfChunksSpinBox.value())
        # for i in range(0,len(self.TimeReadings)-1,self.chunkSizespline):
        #     amplitude = []
        #     time = []
        #     increment = i
        #     for j in range(self.chunkSizespline-1):
        #         if increment < len(self.TimeReadings):
        #             amplitude.append(self.AmplitudeReadings[increment])
        #             time.append(self.TimeReadings[increment])
        #             increment += 1
        #     self.ui.mainGraphGraphicsView.clear()
        #     cubic = interp1d(self.TimeReadings, self.AmplitudeReadings, kind='cubic')
        #     self.ui.mainGraphGraphicsView.plot(self.TimeReadings, self.AmplitudeReadings, pen=pyqtgraph.mkPen('b', width=1.5))
        #     self.ui.mainGraphGraphicsView.plot(self.TimeReadings, cubic(self.TimeReadings), pen=pyqtgraph.mkPen('g', width=1.5, style = QtCore.Qt.DotLine))
    
    def chunkEquations(self, chunkNumber):
        count = 0
        self.chunckSize = ceil(1000/self.ui.polynomialNumberOfChunksSpinBox.value())
        self.order = self.ui.polynomialFittingOrderSpinBox.value()
        for i in range(0,len(self.TimeReadings)-1,self.chunckSize):
            amplitude = []
            time = []
            increment = i
            count +=1
            print(count)
            for j in range(self.chunckSize-1):
                if increment < len(self.TimeReadings):
                    amplitude.append(self.AmplitudeReadings[increment])
                    time.append(self.TimeReadings[increment])
                    increment += 1
            self.coeff = np.polyfit(time[0:int(self.chunckSize-1)], amplitude[0:int(self.chunckSize-1)],self.order)
            if count == chunkNumber:
                return self.coeff


    def interpolationMethods(self):
        self.ui.mainGraphGraphicsView.clear()
        self.ui.mainGraphGraphicsView.plot(self.TimeReadings, self.AmplitudeReadings, pen=pyqtgraph.mkPen('b', width=1.5))
        interpolated_curve_readings, curve_fitting_MSE = self.CurveFitFunctionality(self.ui.polynomialNumberOfChunksSpinBox.value(),self.ui.polynomialOverlapSpinBox.value(),'Polynomial', self.ui.polynomialFittingOrderSpinBox.value(), True)
        self.CurveFittingCoverageCalculation(interpolated_curve_readings)
        self.ui.precentageOfErrorLcdNumber.display(curve_fitting_MSE)
        self.ui.latexEquationComboBox.clear()
        for i in range(1, self.ui.polynomialNumberOfChunksSpinBox.value()+1):
            self.ui.latexEquationComboBox.addItem('Chunk '+ str(i))

    # Sandra's Addition
    def CurveFitFunctionality(self, numberOfChuncks, percentageOfOverlapping, InterpolationKind, InterpolationParameter, plot):

        time_chuncks, signal_chuncks = self.DivisionOfSignalIntoChunksWithOrWithoutOverlapping(numberOfChuncks, percentageOfOverlapping)
        curve_fitting_functions = self.IndividualChunksInterpolation(time_chuncks, signal_chuncks, InterpolationKind, InterpolationParameter)
        interpolated_curve_readings, curve_fitting_MSE = self.GeneratingCurveFittingReadingsAndMSE(numberOfChuncks, percentageOfOverlapping, curve_fitting_functions, time_chuncks, plot)
        return interpolated_curve_readings, curve_fitting_MSE

    def CurveFittingCoverageCalculation(self, interpolated_curve_readings):
        self.signal_curve_fitting_coverage = round( (len(interpolated_curve_readings) / self.number_of_readings) * 100 )
        # FARAH: YOU CAN SET THE LCD HERE 3ALATOOL AND CHANGE FUNCTION NAME ACCORDINGLY MEN8EER MA TRAGA3i 7AGA
        self.ui.CurveFittingCoveragePrecentageLcdNumber.display(self.signal_curve_fitting_coverage)


    def DerivedSignalParametersCalculation(self, numberOfChuncks, percentageOfOverlapping):
        percentageOfOverlapping = round(percentageOfOverlapping/100, 2)
        # derived parameters
        chunck_size = round( self.number_of_readings/numberOfChuncks )
        overlapping_range = round( (self.number_of_readings/numberOfChuncks)*percentageOfOverlapping )
        return chunck_size, overlapping_range

    def DivisionOfSignalIntoChunksWithOrWithoutOverlapping(self, numberOfChuncks, percentageOfOverlapping):

        chunck_size, overlapping_range = self.DerivedSignalParametersCalculation(numberOfChuncks, percentageOfOverlapping)

        # division into chunks with/without overlap
        time_chuncks = [ self.TimeReadings[i:i+chunck_size] for i in range(0, self.number_of_readings - overlapping_range, chunck_size - overlapping_range) ]
        signal_chuncks = [ self.AmplitudeReadings[i:i+chunck_size] for i in range(0, self.number_of_readings - overlapping_range, chunck_size - overlapping_range) ]

        if overlapping_range != 0 and self.prioritizing_constant_number_of_chunks_over_signal_interpolation_coverage:
            time_chuncks = [ time_chuncks[i] for i in range(numberOfChuncks) ]
            signal_chuncks = [ signal_chuncks[i] for i in range(numberOfChuncks) ]

        return time_chuncks, signal_chuncks

    def IndividualChunksInterpolation(self, time_chuncks, signal_chuncks, interpolation_kind, interpolation_parameter):
        if interpolation_kind == 'Polynomial':
            # In polynomial: interpolation parameter is polynomial order
            curve_fitting_functions = [ np.poly1d(np.polyfit(time_chuncks[i], signal_chuncks[i], interpolation_parameter)) for i in range(len(time_chuncks)) ]
        elif interpolation_kind == 'Spline':
            curve_fitting_functions = [ (make_interp_spline(time_chuncks[i], signal_chuncks[i], k=interpolation_parameter)) for i in range(len(time_chuncks))]
        elif interpolation_kind == 'Cubic':
            curve_fitting_functions = [ (interp1d(time_chuncks[i], signal_chuncks[i], kind=interpolation_parameter)) for i in range(len(time_chuncks))]
        return curve_fitting_functions

    def GeneratingCurveFittingReadingsAndMSE(self, numberOfChuncks, percentageOfOverlapping, curve_fitting_functions, time_chuncks, plot):
        chunck_size, overlapping_range = self.DerivedSignalParametersCalculation(numberOfChuncks, percentageOfOverlapping)
        # fitting and averaging(in case of overlap) and plotting
        interpolated_curve_readings = []
        if overlapping_range == 0:
            for i in range(numberOfChuncks):
                interpolated_curve_readings.extend(curve_fitting_functions[i](time_chuncks[i]))
                if plot:
                    # FARAH: PLOTTING COMMAND. EDIT IT AS YOU LIKE
                    self.ui.mainGraphGraphicsView.plot(time_chuncks[i], curve_fitting_functions[i](time_chuncks[i]), pen=pyqtgraph.mkPen('r', width=1.5))
                    pass
        else:
            left_chunk = list(curve_fitting_functions[0](time_chuncks[0]))
            for i in range(len(time_chuncks)-1):
                right_chunk = list(curve_fitting_functions[i+1](time_chuncks[i+1]))
                left_chunk[-overlapping_range:] = np.mean( [ left_chunk[-overlapping_range:], right_chunk[:overlapping_range] ], axis=0 )
                interpolated_curve_readings.extend(left_chunk)
                left_chunk = right_chunk[overlapping_range:]
            interpolated_curve_readings.extend(left_chunk)
            if plot:
                # FARAH: PLOTTING COMMAND. EDIT IT AS YOU LIKE
                self.ui.mainGraphGraphicsView.plot(self.TimeReadings[:len(interpolated_curve_readings)], interpolated_curve_readings, pen=pyqtgraph.mkPen('r', width=1.5))
                pass
        # percentage error calculation
        curve_fitting_MSE = mean_squared_error( self.AmplitudeReadings[:len(interpolated_curve_readings)], interpolated_curve_readings )
        return interpolated_curve_readings, curve_fitting_MSE

    def reportProgress(self, progressValue):
        self.ui.errorMapProgressBar.setValue(progressValue)

    def startThreadRunner(self):
        # Create a runner
        if not self.threadRunning:
            self.worker = Worker(self, self.ui.xAxisComboBox.currentText(), self.ui.yAxisComboBox.currentText(), 5)
            self.threadPaused = False
            self.worker.signals.progress.connect(self.reportProgress)
            self.worker.signals.started.connect(self.start)
            self.worker.signals.finished.connect(self.finish)
            self.threadpool.start(self.worker)
        else:
            self.worker.stop()
            self.threadRunning = False
            self.ui.startAndCancelErrorMapPushButton.setText('Start')
            self.ui.pauseAndRezoomErrorMapPushButton.setEnabled(False)
            self.ui.errorMapProgressBar.setValue(0)

    def finish(self):

        self.threadRunning = False
        self.ui.startAndCancelErrorMapPushButton.setText('Start')
        self.ui.pauseAndRezoomErrorMapPushButton.setEnabled(False)
        self.ui.errorMapProgressBar.setValue(0)

        self.clearErrorMap()

        self.axes = sns.heatmap(self.worker.errors_matrix, cmap="Spectral_r")
        self.axes.set_title("Curve Fitting Percentage Error Map")
        self.axes.set_xticks(range(self.worker.x_axis_parameter_dictionary['Full Range']))
        self.axes.set_yticks(range(self.worker.y_axis_parameter_dictionary['Full Range']))
        self.axes.set_xticklabels( list( np.arange(self.worker.x_axis_parameter_dictionary['Start Range'], self.worker.x_axis_parameter_dictionary['End Range']+1 ) ) )
        self.axes.set_yticklabels( list( np.arange(self.worker.y_axis_parameter_dictionary['End Range'], self.worker.y_axis_parameter_dictionary['Start Range']-1, -1 ) ) )
        self.axes.set( xlabel = self.worker.x_axis_parameter_dictionary['Parameter Name'], ylabel = self.worker.y_axis_parameter_dictionary['Parameter Name'] )

        self.Canvas.draw()

        self.ui.errorMapGraphicsView.show()
        # self.ui.errorLabel.show()

    def start(self):
            self.threadRunning = True
            self.ui.startAndCancelErrorMapPushButton.setText('Cancel')
            self.ui.pauseAndRezoomErrorMapPushButton.setEnabled(True)
            self.ui.errorMapProgressBar.setValue(0)
            self.ui.errorMapProgressBar.show()

    def pauseAndResumeHandler(self):
        if not self.threadPaused:
            self.threadPaused = True
            self.worker.pause_and_resume('Pause')
            self.ui.pauseAndRezoomErrorMapPushButton.setText('Resume')
        else:
            self.threadPaused = False
            self.worker.pause_and_resume('Resume')
            self.ui.pauseAndRezoomErrorMapPushButton.setText('Pause')

    def shutdown(self):
        if self.worker:
            self.worker.stop()

    def render_latex(self,formula, fontsize=12, dpi=300, format_='svg'):
        """Renders LaTeX formula into image.
        """
        fig = plt.figure(figsize=(0.01, 0.01))
        fig.text(0, 0, u'${}$'.format(formula), color='black',fontsize=fontsize)
        buffer_ = BytesIO()
        fig.savefig(buffer_, dpi=dpi, transparent=True, format=format_, bbox_inches='tight', pad_inches=0.0)
        plt.close(fig)
        return buffer_.getvalue()
        


    def equation(self):
        global degree
        if self.isMultiple == False:
            degree = self.ui.polynomialFittingOrderSpinBox.value()
            p = np.polyfit(self.TimeReadings, self.AmplitudeReadings, degree)
            xSymbols = symbols("x")
            poly = sum(S("{:6.2f}".format(v))*xSymbols**i for i, v in enumerate(p[::1]))
            eq_latex = printing.latex(poly)     
            image_bytes = self.render_latex(eq_latex, fontsize=7, dpi=200, format_='png')
            qp = QPixmap()
            qp.loadFromData(image_bytes)
            self.ui.latexEquationLabel.setPixmap(qp)
        elif self.isMultiple == True:
            self.chunkNumber = self.ui.latexEquationComboBox.currentIndex() + 1
            p = self.chunkEquations(self.chunkNumber)
            degree = self.ui.polynomialFittingOrderSpinBox.value()
            xSymbols = symbols("x")
            poly = sum(S("{:6.2f}".format(v))*xSymbols**i for i, v in enumerate(p[::1]))
            eq_latex = printing.latex(poly)     
            image_bytes = self.render_latex(eq_latex, fontsize=7, dpi=200, format_='png')
            qp = QPixmap()
            qp.loadFromData(image_bytes)
            self.ui.latexEquationLabel.setPixmap(qp)



    # Sandra's Addition: General Function
def GetDictionaryByKeyValuePair(dictionaries_list, key_to_search_by, value_to_search_by):
        dictionary_to_find = {}
        for dictionary in dictionaries_list:
            if dictionary[key_to_search_by] == value_to_search_by:
                dictionary_to_find = dictionary
        return dictionary_to_find
    
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())