import logging
import sys; from math import ceil; import numpy as np; import pandas as pd; import matplotlib.pyplot as plt; import seaborn as sns; from re import T; from io import BytesIO
from PyQt5 import QtCore, QtWidgets; from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox; from PyQt5.QtGui import QPixmap; from sympy import S, symbols, printing
from scipy.interpolate import make_interp_spline; from scipy.interpolate import interp1d; from sklearn.metrics import mean_squared_error; from PyQt5.QtCore import QThreadPool
import pyqtgraph; from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas; from GUI import Ui_MainWindow; from ErrorMapWorker import *

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%d-%m-%Y:%H:%M:%S',
                    filename='Logging.txt')

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Variables Initialization
        self.TimeReadings, self.AmplitudeReadings, self.threadpool = [], [], QThreadPool()
        self.number_of_readings, self.chunkNumber, self.interpolationKind = 1000, 1, 'Polynomial'
        self.prioritizing_constant_number_of_chunks_over_signal_interpolation_coverage, self.isMultiple, self.threadRunning, self.threadPaused = False, False, False, False
        self.signal_curve_fitting_coverage, self.error_map_x_axis_parameter, self.error_map_y_axis_parameter = None, None, None
        self.ui.pauseAndResumeErrorMapPushButton.setEnabled(False); self.ui.numberOfChunksSpinBox.setValue(1)
        self.showAndHideCubicSettings = [ {'UI Element': self.ui.multipleChunksRadioButton,'Function': "show"}, {'UI Element': self.ui.fitPushButton,'Function': "show"}, {'UI Element': self.ui.oneChunkRadioButton,'Function': "show"}, {'UI Element': self.ui.CurveFittingCoveragePrecentageLabel,'Function': "show"}, {'UI Element': self.ui.CurveFittingCoveragePrecentageLcdNumber,'Function': "show"}, {'UI Element': self.ui.signalCoveragePrecentageLabel,'Function': "show"}, {'UI Element': self.ui.extrapolationHorizontalSlider,'Function': "show"}, {'UI Element': self.ui.extrapolationLabel,'Function': "show"}, {'UI Element': self.ui.extrapolationPercentageLabel,'Function': "show"}, {'UI Element': self.ui.precentageOfErrorLabel,'Function': "show"},{'UI Element': self.ui.precentageOfErrorLcdNumber,'Function': "show"}, {'UI Element': self.ui.precentageLabel,'Function': "show"}, {'UI Element': self.ui.fittingOrderLabel,'Function': "hide"}, {'UI Element': self.ui.fittingOrderSpinBox,'Function': "hide"}, {'UI Element': self.ui.numberOfChunksSpinBox,'Function': "hide"}, {'UI Element': self.ui.numberOfChunksLabel,'Function': "hide"}, {'UI Element': self.ui.overlapSpinBox,'Function': "hide"}, {'UI Element': self.ui.overlapLabel,'Function': "hide"}, {'UI Element': self.ui.noOverlappingRadioButton,'Function': "hide"}, {'UI Element': self.ui.overlappingRadioButton,'Function': "hide"}, {'UI Element': self.ui.fullCoverageRadioButton,'Function': "hide"}, {'UI Element': self.ui.constantChunkRadioButton,'Function': "hide"} ]
        self.showAndHidePolynomialAndSplineSettings = [ {'UI Element': self.ui.multipleChunksRadioButton, 'Function': "show"}, {'UI Element': self.ui.fitPushButton, 'Function': "show"}, {'UI Element': self.ui.fittingOrderLabel, 'Function': "show"}, {'UI Element': self.ui.fittingOrderSpinBox, 'Function': "show"}, {'UI Element': self.ui.oneChunkRadioButton, 'Function': "show"}, {'UI Element': self.ui.CurveFittingCoveragePrecentageLabel, 'Function': "show"}, {'UI Element': self.ui.CurveFittingCoveragePrecentageLcdNumber, 'Function': "show"}, {'UI Element': self.ui.signalCoveragePrecentageLabel, 'Function': "show"}, {'UI Element': self.ui.extrapolationHorizontalSlider, 'Function': "show"}, {'UI Element': self.ui.extrapolationLabel, 'Function': "show"}, {'UI Element': self.ui.extrapolationPercentageLabel, 'Function': "show"}, {'UI Element': self.ui.precentageOfErrorLabel, 'Function': "show"}, {'UI Element': self.ui.precentageOfErrorLcdNumber, 'Function': "show"}, {'UI Element': self.ui.precentageLabel, 'Function': "show"}, {'UI Element': self.ui.numberOfChunksLabel, 'Function': "hide"}, {'UI Element': self.ui.numberOfChunksSpinBox, 'Function': "hide"}, {'UI Element': self.ui.overlapSpinBox, 'Function': "hide"},{'UI Element': self.ui.overlapLabel, 'Function': "hide"},{'UI Element': self.ui.noOverlappingRadioButton, 'Function': "hide"}, {'UI Element': self.ui.overlappingRadioButton, 'Function': "hide"}, {'UI Element': self.ui.fullCoverageRadioButton, 'Function': "hide"}, {'UI Element': self.ui.constantChunkRadioButton, 'Function': "hide"} ]
        self.showAndHideAllSettings = [ {'UI Element': self.ui.multipleChunksRadioButton, 'Function': "hide"}, {'UI Element': self.ui.fitPushButton, 'Function': "hide"}, {'UI Element': self.ui.fittingOrderLabel, 'Function': "hide"}, {'UI Element': self.ui.fittingOrderSpinBox, 'Function': "hide"}, {'UI Element': self.ui.oneChunkRadioButton, 'Function': "hide"}, {'UI Element': self.ui.numberOfChunksLabel, 'Function': "hide"}, {'UI Element': self.ui.numberOfChunksSpinBox, 'Function': "hide"}, {'UI Element': self.ui.noOverlappingRadioButton, 'Function': "hide"}, {'UI Element': self.ui.overlapSpinBox, 'Function': "hide"}, {'UI Element': self.ui.overlapLabel, 'Function': "hide"}, {'UI Element': self.ui.fullCoverageRadioButton, 'Function': "hide"}, {'UI Element': self.ui.constantChunkRadioButton, 'Function': "hide"}, {'UI Element': self.ui.CurveFittingCoveragePrecentageLabel, 'Function': "hide"}, {'UI Element': self.ui.CurveFittingCoveragePrecentageLcdNumber, 'Function': "hide"}, {'UI Element': self.ui.extrapolationHorizontalSlider, 'Function': "hide"}, {'UI Element': self.ui.extrapolationLabel, 'Function': "hide"}, {'UI Element': self.ui.extrapolationPercentageLabel, 'Function': "hide"}, {'UI Element': self.ui.precentageOfErrorLabel, 'Function': "hide"}, {'UI Element': self.ui.precentageOfErrorLcdNumber, 'Function': "hide"}, {'UI Element': self.ui.precentageLabel, 'Function': "hide"}, {'UI Element': self.ui.signalCoveragePrecentageLabel, 'Function': "hide"}, {'UI Element': self.ui.errorMapGraphicsView, 'Function': "hide"}, {'UI Element': self.ui.errorMapProgressBar, 'Function': "hide"}, {'UI Element': self.ui.overlappingRadioButton, 'Function': "hide"} ]
        self.overlapSettings, self.chunksNumberSettings = [self.ui.overlapSpinBox, self.ui.overlapLabel, self.ui.fullCoverageRadioButton, self.ui.constantChunkRadioButton], [self.ui.numberOfChunksLabel, self.ui.numberOfChunksSpinBox, self.ui.noOverlappingRadioButton, self.ui.overlappingRadioButton]
        self.errorMapComboBoxesAxesList = [ {'Current Axis Text': 'Choose Axis Parameter', 'Axis List': ["Choose Axis Parameter", "Number of Chunks", "Polynomial Order", "Overlapping Percentage"]}, {'Current Axis Text': 'Polynomial Order', 'Axis List': ["Choose Axis Parameter", "Number of Chunks", "Overlapping Percentage"]}, {'Current Axis Text': 'Number of Chunks', 'Axis List': ["Choose Axis Parameter", "Polynomial Order", "Overlapping Percentage"]}, {'Current Axis Text': 'Overlapping Percentage', 'Axis List': ["Choose Axis Parameter", "Number of Chunks", "Polynomial Order"]} ]
        self.constantParameterSettingDictionaryList = [{'X-Axis': "Number of Chunks", 'Y-Axis': "Polynomial Order", 'Constant Parameter': "Overlapping Percentage", 'Minimum': 0,'Maximum': 25,'Value': 0}, {'X-Axis': "Polynomial Order", 'Y-Axis': "Number of Chunks", 'Constant Parameter': "Overlapping Percentage", 'Minimum': 0,'Maximum': 25,'Value': 0}, {'X-Axis': "Number of Chunks", 'Y-Axis': "Overlapping Percentage", 'Constant Parameter': "Polynomial Order", 'Minimum': 0,'Maximum': 10,'Value': 0}, {'X-Axis': "Overlapping Percentage", 'Y-Axis': "Number of Chunks", 'Constant Parameter': "Polynomial Order", 'Minimum': 0,'Maximum': 10,'Value': 0}, {'X-Axis': "Polynomial Order", 'Y-Axis': "Overlapping Percentage", 'Constant Parameter': "Number of Chunks", 'Minimum': 1,'Maximum': 20,'Value': 1}, {'X-Axis': "Overlapping Percentage", 'Y-Axis': "Polynomial Order", 'Constant Parameter': "Number of Chunks", 'Minimum': 1,'Maximum': 20,'Value': 1}]
        self.spinBoxesInitializationList = [ {'One Chunk Case': True, 'Settings':[(self.ui.overlapSpinBox, 0), (self.ui.numberOfChunksSpinBox, 1)]}, {'One Chunk Case': False, 'Settings':[(self.ui.overlapSpinBox, 0), (self.ui.numberOfChunksSpinBox, 1), (self.ui.fittingOrderSpinBox, 0)]} ]
        self.UIElementsAndFunctions = [ {'UI Element': self.ui.multipleChunksRadioButton.toggled,'Function': self.ChunksNumberRadioButtonsCheck}, {'UI Element': self.ui.oneChunkRadioButton.toggled,'Function': self.ChunksNumberRadioButtonsCheck}, {'UI Element': self.ui.polynomialRadioButton.toggled,'Function': self.interpolationMethodsRadioButton}, {'UI Element': self.ui.splineRadioButton.toggled,'Function': self.interpolationMethodsRadioButton}, {'UI Element': self.ui.overlappingRadioButton.toggled,'Function': self.OverlapRadioButtonsCheck}, {'UI Element': self.ui.noOverlappingRadioButton.toggled,'Function': self.OverlapRadioButtonsCheck}, {'UI Element': self.ui.constantChunkRadioButton.toggled,'Function': self.FullFittingCoverageAndConstantChunksNumberSettings}, {'UI Element': self.ui.cubicRadioButton.toggled,'Function': self.interpolationMethodsRadioButton}, {'UI Element': self.ui.startAndCancelErrorMapPushButton.pressed,'Function': self.startThreadRunner}, {'UI Element': self.ui.pauseAndResumeErrorMapPushButton.pressed,'Function': self.pauseAndResumeHandler}, {'UI Element': self.ui.openAction.triggered,'Function': self.OpenFile}, {'UI Element': self.ui.fitPushButton.clicked,'Function': self.interpolationMethods}, {'UI Element': self.ui.xAxisComboBox.textActivated,'Function': lambda:self.ErrorMapAxesComboBoxesSetter("X-Axis")}, {'UI Element': self.ui.yAxisComboBox.textActivated,'Function': lambda:self.ErrorMapAxesComboBoxesSetter("Y-Axis")}, {'UI Element': self.ui.extrapolationHorizontalSlider.valueChanged,'Function': self.extrapolation}, {'UI Element': self.ui.fittingOrderSpinBox.valueChanged,'Function': self.equation}, {'UI Element': self.ui.latexEquationComboBox.currentIndexChanged,'Function': self.equation}]
        for UIElementDictionary in self.UIElementsAndFunctions:
            UIElementDictionary['UI Element'].connect(UIElementDictionary['Function'])
        self.ui.xAxisComboBox.setCurrentText("Number of Chunks"); self.ErrorMapAxesComboBoxesSetter("X-Axis"); self.ui.yAxisComboBox.setCurrentText("Polynomial Order"); self.ErrorMapAxesComboBoxesSetter("Y-Axis"); self.showAndHide('all')

    # Methods
    def OpenFile(self):
        self.file_name = QtWidgets.QFileDialog.getOpenFileName(caption="Choose Signal", directory="", filter="csv (*.csv)")[0]; self.data_frame = pd.read_csv(self.file_name, encoding = 'utf-8').fillna(0)
        self.TimeReadings, self.AmplitudeReadings = self.data_frame.iloc[:,0].to_numpy(), self.data_frame.iloc[:,1].to_numpy()
        self.ui.mainGraphGraphicsView.clear(); self.ui.mainGraphGraphicsView.setYRange(min(self.AmplitudeReadings), max(self.AmplitudeReadings))
        self.ui.mainGraphGraphicsView.plot(self.TimeReadings, self.AmplitudeReadings, pen=pyqtgraph.mkPen('b', width=1.5))
        logging.info('User opening a File')

    def interpolationMethodsRadioButton(self):
        if self.ui.polynomialRadioButton.isChecked(): self.SetInterpolationMethod('Polynomial')
        elif self.ui.splineRadioButton.isChecked(): self.SetInterpolationMethod('Spline')
        elif self.ui.cubicRadioButton.isChecked(): self.SetInterpolationMethod('Cubic')

    def SetInterpolationMethod(self, interpolationKind):
        self.interpolationKind = interpolationKind; self.showAndHide(self.interpolationKind); self.setSpinBox(False)

    def ChunksNumberRadioButtonsCheck(self):
        if self.ui.multipleChunksRadioButton.isChecked(): self.ui.oneChunkRadioButton.show(); self.isMultiple = True; self.ShowAndHideOverlapOrChunksNumberSettings("show", self.chunksNumberSettings)
        elif self.ui.oneChunkRadioButton.isChecked(): self.setSpinBox(True); self.isMultiple = False; self.ShowAndHideOverlapOrChunksNumberSettings("hide", self.overlapSettings); self.ShowAndHideOverlapOrChunksNumberSettings("hide", self.chunksNumberSettings)
        logging.info('Choosing multiple chunks')

    def OverlapRadioButtonsCheck(self):
        if self.ui.overlappingRadioButton.isChecked(): self.ShowAndHideOverlapOrChunksNumberSettings("show", self.overlapSettings)
        elif self.ui.noOverlappingRadioButton.isChecked(): self.ShowAndHideOverlapOrChunksNumberSettings("hide", self.overlapSettings)
        logging.info('Choosing overlapping')

    def ShowAndHideOverlapOrChunksNumberSettings(self, displayMethod, overlapOrChunksNumberSettings):
        for overlapOrChunksNumberSettings in overlapOrChunksNumberSettings:
             getattr(overlapOrChunksNumberSettings, displayMethod)()

    def showAndHide(self, show):
        if show == 'Cubic': self.ShowAndHideInterpolationSettings(self.showAndHideCubicSettings)
        elif show == 'Polynomial' or show == 'Spline': self.ShowAndHideInterpolationSettings(self.showAndHidePolynomialAndSplineSettings)
        elif show == 'all': self.ShowAndHideInterpolationSettings(self.showAndHideAllSettings)

    def ShowAndHideInterpolationSettings(self, settingsList):
        for Setting in settingsList:
            getattr(Setting['UI Element'], Setting['Function'])()

    def ErrorMapAxesComboBoxesSetter(self, axisType):
        if axisType == "X-Axis": self.ErrorMapAxesComboBoxesHelperFunction(self.ui.xAxisComboBox, self.ui.yAxisComboBox)
        elif axisType == "Y-Axis": self.ErrorMapAxesComboBoxesHelperFunction(self.ui.yAxisComboBox, self.ui.xAxisComboBox)
        logging.info('Choosing axes for the error map')

    def ErrorMapAxesComboBoxesHelperFunction(self, currentAxisComboBox, otherAxisComboBox):
        otherAxisText, currentAxisText = otherAxisComboBox.currentText(), currentAxisComboBox.currentText()
        comboBoxAxisList = GetDictionaryByKeyValuePair(self.errorMapComboBoxesAxesList, 'Current Axis Text', currentAxisText)
        otherAxisComboBox.clear(); otherAxisComboBox.addItems(comboBoxAxisList["Axis List"]); otherAxisComboBox.setCurrentText(otherAxisText); self.ConstantParameterSetting()

    def ConstantParameterSetting(self):
        if self.ui.xAxisComboBox.currentText() != 'Choose Axis Parameter' and self.ui.yAxisComboBox.currentText() != 'Choose Axis Parameter':
            xAxisCurrentText, yAxisCurrentText = self.ui.xAxisComboBox.currentText(), self.ui.yAxisComboBox.currentText()
            constantParameter = GetDictionaryByTwoKeyValuePairs(self.constantParameterSettingDictionaryList, 'X-Axis', xAxisCurrentText, 'Y-Axis', yAxisCurrentText)
            self.ui.constantParameterLabel.setText(constantParameter['Constant Parameter']); self.ui.constantParameterSpinBox.setMinimum(constantParameter['Minimum']); self.ui.constantParameterSpinBox.setMaximum(constantParameter['Maximum']); self.ui.constantParameterSpinBox.setValue(constantParameter['Value'])

    def FullFittingCoverageAndConstantChunksNumberSettings(self):
        if self.ui.constantChunkRadioButton.isChecked(): messageBoxElement = QMessageBox.warning(self, 'Warning!', "Signal Curve Fitting Coverage may not be 100%.\nThis applies to Curve Fitting Functionality as well as Error Map Calculation (Polynomial Case)."); self.prioritizing_constant_number_of_chunks_over_signal_interpolation_coverage = True
        elif self.ui.fullCoverageRadioButton.isChecked(): messageBoxElement = QMessageBox.warning(self, 'Warning!', "User Input's Number of Chunks may not be kept Constant.\nThis applies to Curve Fitting Functionality as well as Error Map Calculation (Polynomial Case)."); self.prioritizing_constant_number_of_chunks_over_signal_interpolation_coverage = False
        logging.info('Showing error messages according to overlap settings chosen')

    def setSpinBox(self, one):
        spinBoxSettings = GetDictionaryByKeyValuePair(self.spinBoxesInitializationList, 'One Chunk Case', one)
        for spinBox in spinBoxSettings['Settings']:
            spinBox[0].setValue(spinBox[1])

    def extrapolation(self):
        self.extrapolationSliderValue = self.ui.extrapolationHorizontalSlider.value()
        self.ui.extrapolationPercentageLabel.setText(f'{self.extrapolationSliderValue}% Original Signal')
        self.lastIndex= int((self.extrapolationSliderValue/100)* len(self.TimeReadings))
        self.order, amplitude, time, residualTime, extrapolatedAmplitude = self.ui.fittingOrderSpinBox.value(), [], [], [], []
        time, amplitude, residualTime = self.TimeReadings[0:self.lastIndex], self.AmplitudeReadings[0:self.lastIndex], self.TimeReadings[self.lastIndex:len(self.TimeReadings)]     
        self.coeff = np.polyfit(time, amplitude,self.order); self.poly1d_fn, extrapolatedAmplitude = np.poly1d(self.coeff), np.polyval(self.coeff, residualTime)  
        self.ui.mainGraphGraphicsView.clear(); self.ui.mainGraphGraphicsView.plot(self.TimeReadings, self.AmplitudeReadings, pen=pyqtgraph.mkPen('b', width=1.5))
        self.ui.mainGraphGraphicsView.plot(time, self.poly1d_fn(time), pen=pyqtgraph.mkPen('g', width=1.5, style = QtCore.Qt.DotLine)); self.ui.mainGraphGraphicsView.plot(residualTime, extrapolatedAmplitude, pen=pyqtgraph.mkPen('r', width=1.5, style = QtCore.Qt.DotLine))
        logging.info('Using the extrapolation slider')

    def clearErrorMap(self):
        self.figure = plt.figure(figsize=(15,5)); self.axes = self.figure.get_axes()
        self.Canvas = FigureCanvas(self.figure); self.ui.errorMapGridLayout.addWidget(self.Canvas,0, 0, 1, 1)

    def chunkEquations(self, chunkNumber):
        count, self.chunckSize, self.order = 0, ceil(1000/self.ui.numberOfChunksSpinBox.value()), self.ui.fittingOrderSpinBox.value()
        for i in range(0,len(self.TimeReadings)-1,self.chunckSize):
            amplitude, time, increment = [], [], i; count +=1
            for j in range(self.chunckSize-1):
                if increment < len(self.TimeReadings): amplitude.append(self.AmplitudeReadings[increment]); time.append(self.TimeReadings[increment]); increment += 1
            self.coeff = np.polyfit(time[0:int(self.chunckSize-1)], amplitude[0:int(self.chunckSize-1)],self.order)
            if count == chunkNumber: return self.coeff
        logging.info('Showing each chunk equation')

    def interpolationMethods(self):
        self.ui.mainGraphGraphicsView.clear(); self.ui.mainGraphGraphicsView.plot(self.TimeReadings, self.AmplitudeReadings, pen=pyqtgraph.mkPen('b', width=1.5))
        if self.interpolationKind == 'Polynomial':
            self.ui.latexEquationComboBox.clear()
            for i in range(1, self.ui.numberOfChunksSpinBox.value()+1):
                self.ui.latexEquationComboBox.addItem('Chunk '+ str(i))
        elif self.interpolationKind == 'Spline':
            if self.ui.fittingOrderSpinBox.value() % 2 == 0 and self.ui.fittingOrderSpinBox.value() != 2 : messageBoxElement = QMessageBox.warning(self, "Error!", 'Spline degree must be odd number or 2 \n Please enter an odd number'); self.ui.fittingOrderSpinBox.setValue(1)
        interpolated_curve_readings, curve_fitting_MSE = self.CurveFitFunctionality(self.ui.numberOfChunksSpinBox.value(),self.ui.overlapSpinBox.value(), self.interpolationKind, self.ui.fittingOrderSpinBox.value(), True)
        self.CurveFittingCoverageCalculation(interpolated_curve_readings); self.ui.precentageOfErrorLcdNumber.display(round(curve_fitting_MSE, 2))

    def CurveFitFunctionality(self, numberOfChuncks, percentageOfOverlapping, InterpolationKind, InterpolationParameter, plot):
        time_chuncks, signal_chuncks = self.DivisionOfSignalIntoChunksWithOrWithoutOverlapping(numberOfChuncks, percentageOfOverlapping)
        curve_fitting_functions = self.IndividualChunksInterpolation(time_chuncks, signal_chuncks, InterpolationKind, InterpolationParameter)
        interpolated_curve_readings, curve_fitting_MSE = self.GeneratingCurveFittingReadingsAndMSE(numberOfChuncks, percentageOfOverlapping, curve_fitting_functions, time_chuncks, plot)
        return interpolated_curve_readings, curve_fitting_MSE

    def CurveFittingCoverageCalculation(self, interpolated_curve_readings):
        self.signal_curve_fitting_coverage = round( (len(interpolated_curve_readings) / self.number_of_readings) * 100 )
        self.ui.CurveFittingCoveragePrecentageLcdNumber.display(self.signal_curve_fitting_coverage)

    def DerivedSignalParametersCalculation(self, numberOfChuncks, percentageOfOverlapping):
        percentageOfOverlapping, chunck_size, overlapping_range = round(percentageOfOverlapping/100, 2), round( self.number_of_readings/numberOfChuncks ), round( (self.number_of_readings/numberOfChuncks)*percentageOfOverlapping )
        return chunck_size, overlapping_range

    def DivisionOfSignalIntoChunksWithOrWithoutOverlapping(self, numberOfChuncks, percentageOfOverlapping):
        chunck_size, overlapping_range = self.DerivedSignalParametersCalculation(numberOfChuncks, percentageOfOverlapping)
        time_chuncks = [ self.TimeReadings[i:i+chunck_size] for i in range(0, self.number_of_readings - overlapping_range, chunck_size - overlapping_range) ]; signal_chuncks = [ self.AmplitudeReadings[i:i+chunck_size] for i in range(0, self.number_of_readings - overlapping_range, chunck_size - overlapping_range) ]
        if overlapping_range != 0 and self.prioritizing_constant_number_of_chunks_over_signal_interpolation_coverage: time_chuncks = [ time_chuncks[i] for i in range(numberOfChuncks) ]; signal_chuncks = [ signal_chuncks[i] for i in range(numberOfChuncks) ]
        return time_chuncks, signal_chuncks

    def IndividualChunksInterpolation(self, time_chuncks, signal_chuncks, interpolation_kind, interpolation_parameter):
        if interpolation_kind == 'Polynomial': curve_fitting_functions = [ np.poly1d(np.polyfit(time_chuncks[i], signal_chuncks[i], interpolation_parameter)) for i in range(len(time_chuncks)) ]
        elif interpolation_kind == 'Spline': curve_fitting_functions = [ (make_interp_spline(time_chuncks[i], signal_chuncks[i], k=interpolation_parameter)) for i in range(len(time_chuncks))]
        elif interpolation_kind == 'Cubic': curve_fitting_functions = [ (interp1d(time_chuncks[i], signal_chuncks[i], kind='cubic')) for i in range(len(time_chuncks))]
        return curve_fitting_functions

    def GeneratingCurveFittingReadingsAndMSE(self, numberOfChuncks, percentageOfOverlapping, curve_fitting_functions, time_chuncks, plot):
        chunck_size, overlapping_range = self.DerivedSignalParametersCalculation(numberOfChuncks, percentageOfOverlapping); interpolated_curve_readings = []
        if overlapping_range == 0:
            for i in range(numberOfChuncks):
                interpolated_curve_readings.extend(curve_fitting_functions[i](time_chuncks[i]))
                if plot: self.ui.mainGraphGraphicsView.plot(time_chuncks[i], curve_fitting_functions[i](time_chuncks[i]), pen=pyqtgraph.mkPen('r', width=1.5))
        else:
            left_chunk = list(curve_fitting_functions[0](time_chuncks[0]))
            for i in range(len(time_chuncks)-1):
                right_chunk = list(curve_fitting_functions[i+1](time_chuncks[i+1])); left_chunk[-overlapping_range:] = np.mean( [ left_chunk[-overlapping_range:], right_chunk[:overlapping_range] ], axis=0 )
                interpolated_curve_readings.extend(left_chunk); left_chunk = right_chunk[overlapping_range:]
            interpolated_curve_readings.extend(left_chunk)
            if plot: self.ui.mainGraphGraphicsView.plot(self.TimeReadings[:len(interpolated_curve_readings)], interpolated_curve_readings, pen=pyqtgraph.mkPen('r', width=1.5))
        curve_fitting_MSE = mean_squared_error( self.AmplitudeReadings[:len(interpolated_curve_readings)], interpolated_curve_readings )
        return interpolated_curve_readings, curve_fitting_MSE*100

    def reportProgress(self, progressValue): self.ui.errorMapProgressBar.setValue(progressValue)

    def ErrorMapStartAndEndSettings(self, threadRunningValue, startAndCancelErrorMapButtonText, pauseAndResumeErrorMapButtonDisplay):
        self.threadRunning = threadRunningValue; self.ui.startAndCancelErrorMapPushButton.setText(startAndCancelErrorMapButtonText)
        self.ui.pauseAndResumeErrorMapPushButton.setEnabled(pauseAndResumeErrorMapButtonDisplay); self.ui.errorMapProgressBar.setValue(0)
        logging.info('Error map progress bar')

    def ErrorMapPauseAndResumeSettings(self, threadPausedValue, mode, pauseAndResumeErrorMapButtonText):
        self.threadPaused = threadPausedValue; self.worker.pause_and_resume(mode)
        self.ui.pauseAndResumeErrorMapPushButton.setText(pauseAndResumeErrorMapButtonText)
        logging.info('Error map pause/resume')

    def startThreadRunner(self):
        if not self.threadRunning:
            self.worker = ErrorMapWorker(self, self.ui.xAxisComboBox.currentText(), self.ui.yAxisComboBox.currentText(), self.ui.constantParameterSpinBox.value()); self.threadPaused = False
            self.errorMapWorkerSignalSettings = [{'Signal': self.worker.ErrorMapWorkerSignals.ErrorMapProgressSignal, 'Function': self.reportProgress}, {'Signal':self.worker.ErrorMapWorkerSignals.ErrorMapStartedSignal, 'Function': self.start}, {'Signal':self.worker.ErrorMapWorkerSignals.ErrorMapFinishedSignal, 'Function': self.finish}]
            for errorMapWorkerSignalSetting in self.errorMapWorkerSignalSettings:
                errorMapWorkerSignalSetting['Signal'].connect(errorMapWorkerSignalSetting['Function'])
            self.threadpool.start(self.worker)
        else: self.worker.stop(); self.ErrorMapStartAndEndSettings(False, 'Start', False)

    def finish(self):
        self.ErrorMapStartAndEndSettings(False, 'Start', False); self.clearErrorMap()
        self.axes = sns.heatmap(self.worker.errors_matrix, cmap="Spectral_r")
        self.axes.set_title("Curve Fitting Percentage Error Map"); self.axes.set_xticks(range(self.worker.x_axis_parameter_dictionary['Full Range'])); self.axes.set_yticks(range(self.worker.y_axis_parameter_dictionary['Full Range']))
        self.axes.set_xticklabels( list( np.arange(self.worker.x_axis_parameter_dictionary['Start Range'], self.worker.x_axis_parameter_dictionary['End Range']+1 ) ) ); self.axes.set_yticklabels( list( np.arange(self.worker.y_axis_parameter_dictionary['End Range'], self.worker.y_axis_parameter_dictionary['Start Range']-1, -1 ) ) )
        self.axes.set( xlabel = self.worker.x_axis_parameter_dictionary['Parameter Name'], ylabel = self.worker.y_axis_parameter_dictionary['Parameter Name'] ); self.Canvas.draw()
        errorMapSpacer = QtWidgets.QSpacerItem(550, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum); self.ui.errorMapGridLayout.addItem(errorMapSpacer, 1, 0, 1, 1)
        
    def start(self):
        self.ErrorMapStartAndEndSettings(True, 'Cancel', True); self.ui.errorMapProgressBar.show()
        logging.info('Start error map')

    def pauseAndResumeHandler(self):
        if not self.threadPaused: self.ErrorMapPauseAndResumeSettings(True, 'Pause', 'Resume')
        else: self.ErrorMapPauseAndResumeSettings(False, 'Resume', 'Pause')

    def shutdown(self):
        if self.worker: self.worker.stop()

    def render_latex(self,formula, fontsize=12, dpi=300, format_='svg'):
        fig = plt.figure(figsize=(0.01, 0.01)); fig.text(0, 0, u'${}$'.format(formula), color='black',fontsize=fontsize)
        buffer_ = BytesIO(); fig.savefig(buffer_, dpi=dpi, transparent=True, format=format_, bbox_inches='tight', pad_inches=0.0)
        plt.close(fig); return buffer_.getvalue()
        
    def equation(self):
        global degree
        if self.isMultiple == False:
            degree, coeff = self.ui.fittingOrderSpinBox.value(), np.polyfit(self.TimeReadings, self.AmplitudeReadings, degree); p, xSymbols = coeff[::-1], symbols("x")
            poly = sum(S("{:6.2f}".format(v))*xSymbols**i for i, v in enumerate(p[::1])); eq_latex = printing.latex(poly)     
            image_bytes = self.render_latex(eq_latex, fontsize=7, dpi=200, format_='png'); qp = QPixmap(); qp.loadFromData(image_bytes); self.ui.latexEquationLabel.setPixmap(qp)
        elif self.isMultiple == True:
            self.chunkNumber, p = self.ui.latexEquationComboBox.currentIndex() + 1, self.chunkEquations(self.chunkNumber)
            degree, xSymbols = self.ui.fittingOrderSpinBox.value(), symbols("x"); poly = sum(S("{:6.2f}".format(v))*xSymbols**i for i, v in enumerate(p[::1]))
            eq_latex = printing.latex(poly); image_bytes = self.render_latex(eq_latex, fontsize=7, dpi=200, format_='png'); qp = QPixmap(); qp.loadFromData(image_bytes); self.ui.latexEquationLabel.setPixmap(qp)
        logging.info('Show interpolation equation')

def GetDictionaryByTwoKeyValuePairs(dictionaries_list, first_key_to_search_by, first_value_to_search_by, second_key_to_search_by, second_value_to_search_by):
        dictionary_to_find = {}
        for dictionary in dictionaries_list:
            if dictionary[first_key_to_search_by] == first_value_to_search_by and dictionary[second_key_to_search_by] == second_value_to_search_by: dictionary_to_find = dictionary
        return dictionary_to_find
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
