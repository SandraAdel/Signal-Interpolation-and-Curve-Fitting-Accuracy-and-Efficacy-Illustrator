from ast import increment_lineno
from configparser import Interpolation
from math import ceil
import sys
from turtle import title
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import pyqtgraph
from pyqtgraph import PlotWidget
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from GUI2 import Ui_MainWindow
import seaborn as sns
from sklearn.metrics import mean_squared_error
from PyQt5.QtWidgets import QWidget, QApplication, QProgressBar, QMainWindow, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot, QRunnable, QThreadPool
import time
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.image as mpimg


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
        x_axis_parameter_dictionary = GetDictionaryByKeyValuePair(self.curve_fitting_parameters_list, 'Parameter Name', self.x_axis_parameter)
        y_axis_parameter_dictionary = GetDictionaryByKeyValuePair(self.curve_fitting_parameters_list, 'Parameter Name', self.y_axis_parameter)
        number_of_chunks_range_on_error_map = self.AssignLoopingRangeForCurveFittingParameters( GetDictionaryByKeyValuePair(self.curve_fitting_parameters_list, 'Parameter Name', 'Number of Chunks'), self.x_axis_parameter, self.y_axis_parameter, self.constant_parameter_value )
        overlapping_percentage_range_on_error_map = self.AssignLoopingRangeForCurveFittingParameters( GetDictionaryByKeyValuePair(self.curve_fitting_parameters_list, 'Parameter Name', 'Overlapping Percentage'), self.x_axis_parameter, self.y_axis_parameter, self.constant_parameter_value )
        polynomial_order_range_on_error_map = self.AssignLoopingRangeForCurveFittingParameters( GetDictionaryByKeyValuePair(self.curve_fitting_parameters_list, 'Parameter Name', 'Polynomial Order'), self.x_axis_parameter, self.y_axis_parameter, self.constant_parameter_value )
        errors_matrix = np.zeros(( y_axis_parameter_dictionary['Full Range'] , x_axis_parameter_dictionary['Full Range'] ))
        progress_step = 100/(errors_matrix.size)
        row_index = y_axis_parameter_dictionary['Full Range'] - 1
        column_index = 0
        for overlapping_percentage in range(overlapping_percentage_range_on_error_map[0], overlapping_percentage_range_on_error_map[1]+1):
            for polynomial_order in range(polynomial_order_range_on_error_map[0], polynomial_order_range_on_error_map[1]+1):
                for number_of_chunks in range(number_of_chunks_range_on_error_map[0], number_of_chunks_range_on_error_map[1]+1):
                    __ , MSE_error = self.window_object.CurveFitFunctionality(number_of_chunks, overlapping_percentage, 'Polynomial', polynomial_order, False)
                    errors_matrix[ row_index, column_index ] = MSE_error
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
                    row_index = y_axis_parameter_dictionary['Full Range'] - 1
                if self.x_axis_parameter == 'Polynomial Order' and self.y_axis_parameter != 'Number of Chunks':
                    column_index += 1
                elif self.y_axis_parameter == 'Polynomial Order'and self.x_axis_parameter != 'Number of Chunks':
                    row_index -= 1
            if self.x_axis_parameter == 'Polynomial Order':
                column_index = 0
                row_index -= 1
            elif self.y_axis_parameter == 'Polynomial Order':
                column_index += 1
                row_index = y_axis_parameter_dictionary['Full Range'] - 1

        ax = sns.heatmap(errors_matrix, cmap="Spectral_r")
        ax.set_title("Curve Fitting Percentage Error Map")
        ax.set_xticks(range(x_axis_parameter_dictionary['Full Range']))
        ax.set_yticks(range(y_axis_parameter_dictionary['Full Range']))
        ax.set_xticklabels( list( np.arange(x_axis_parameter_dictionary['Start Range'], x_axis_parameter_dictionary['End Range']+1 ) ) )
        ax.set_yticklabels( list( np.arange(y_axis_parameter_dictionary['End Range'], y_axis_parameter_dictionary['Start Range']-1, -1 ) ) )
        ax.set( xlabel = x_axis_parameter_dictionary['Parameter Name'], ylabel = y_axis_parameter_dictionary['Parameter Name'] )

        plt.savefig('Error_Map.png', dpi = 300 ,bbox_inches='tight')

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
        self.TimeReadings = None
        self.AmplitudeReadings = None
        self.chunkSize = 0
        self.oneChunk = 0
        self.result = []

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

        #self.fig = Figure()
        #self.ax = self.fig.add_subplot(111)
        #self.canvas = FigureCanvas(self.fig)
        #self.canvas.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        #self.canvas.updateGeometry()
        #self.ui.errorMapGridLayout.addWidget(self.canvas,0, 0, 1, 1)


        self.ui.polynomialNumberOfChunksSpinBox.setValue(1)
        # Hide error map elements
        self.ui.errorMapGraphicsView.hide()
        self.ui.errorLabel.hide()
        self.ui.errorMapProgressBar.hide()
        self.ui.errorMapProgressBar.setValue(0)
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
        # self.ui.yAxisComboBox.currentIndexChanged.connect(lambda: self.yAxis())
        self.ui.polynomialOverlappingRadioButton.toggled.connect(lambda: self.polynomialOverlapRadioButton())
        self.ui.polynomialNoOverlappingRadioButton.toggled.connect(lambda: self.polynomialNoOverlapRadioButton())
        self.ui.polynomialConstantChunkRadioButton.toggled.connect(lambda: self.keepConstantChunkRadioButton())
        self.ui.polynomialFullCoverageRadioButton.toggled.connect(lambda: self.FullCoverageRadioButton())

    # Methods
    def OpenFile(self):
        self.file_name = QtWidgets.QFileDialog.getOpenFileName(caption="Choose Signal", directory="", filter="csv (*.csv)")[0]
        data_frame = pd.read_csv(self.file_name, encoding = 'utf-8').fillna(0)
        self.TimeReadings = list(data_frame.iloc[:,0])
        self.AmplitudeReadings = list(data_frame.iloc[:,1])
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

    def FullCoverageRadioButton(self):
        if self.ui.polynomialFullCoverageRadioButton.isChecked():
            self.ShowPopUpMessage("User input's number of chunks may not be kept constant.") 
            self.prioritizing_constant_number_of_chunks_over_signal_interpolation_coverage = False

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

    def clearErrorMap(self):
        self.figure, self.axes = plt.figure(figsize=(15,5))
        self.Canvas = FigureCanvas(self.figure)
        self.ui.errorMapGridLayout.addWidget(self.Canvas,0, 0, 1, 1)

    #################################################
    # Sandra's Addition
    def CurveFitFunctionality(self, numberOfChuncks, percentageOfOverlapping, InterpolationKind, InterpolationParameter, plot):

        time_chuncks, signal_chuncks = self.DivisionOfSignalIntoChunksWithOrWithoutOverlapping(numberOfChuncks, percentageOfOverlapping)
        curve_fitting_functions = self.IndividualChunksInterpolation(time_chuncks, signal_chuncks, InterpolationKind, InterpolationParameter)
        interpolated_curve_readings, curve_fitting_MSE = self.GeneratingCurveFittingReadingsAndMSE(numberOfChuncks, percentageOfOverlapping, curve_fitting_functions, time_chuncks, plot)
        return interpolated_curve_readings, curve_fitting_MSE

    def CurveFittingCoverageCalculation(self, interpolated_curve_readings):
        self.signal_curve_fitting_coverage = round( (len(interpolated_curve_readings) / self.number_of_readings) * 100 )
        # FARAH: YOU CAN SET THE LCD HERE 3ALATOOL AND CHANGE FUNCTION NAME ACCORDINGLY MEN8EER MA TRAGA3i 7AGA

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
        img_arr = mpimg.imread('Error_Map.png')
        # SANDRA REMINDER: CLEAR canvas before writting !!
        self.ui.errorMapGraphicsView.canvas.ax.axis('off')
        self.ui.errorMapGraphicsView.canvas.fig.subplots_adjust(0,0,1,1)
        self.ui.errorMapGraphicsView.canvas.ax.imshow(img_arr)
        self.ui.errorMapGraphicsView.canvas.draw()

    def start(self):
        self.threadRunning = True
        self.ui.startAndCancelErrorMapPushButton.setText('Cancel')
        self.ui.pauseAndRezoomErrorMapPushButton.setEnabled(True)
        self.ui.errorMapProgressBar.setValue(0)
        self.ui.errorMapGraphicsView.show()
        self.ui.errorLabel.show()
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
    app.aboutToQuit.connect(win.shutdown)
    sys.exit(app.exec_())