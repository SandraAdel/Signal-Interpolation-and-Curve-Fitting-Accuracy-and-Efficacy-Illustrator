
                                                    # # # # # # # # # # Imports # # # # # # # # # #
                                                    
import sys, os; sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sys; from math import ceil; import numpy as np; import pandas as pd; import matplotlib.pyplot as plt; import seaborn as sns; from re import T; from io import BytesIO
from PyQt5 import QtCore, QtWidgets; from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox; from PyQt5.QtGui import QPixmap; from sympy import S, symbols, printing
from scipy.interpolate import make_interp_spline; from scipy.interpolate import interp1d; from sklearn.metrics import mean_squared_error; from PyQt5.QtCore import QThreadPool
import pyqtgraph; from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas; from GUI import Ui_MainWindow; from ErrorMapWorker import *; import logging

                                                    # # # # # # # # # # Logging Setup # # # # # # # # # #

logger = logging.getLogger(); logger.setLevel(logging.INFO); logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s', datefmt='%d-%m-%Y:%H:%M:%S', filename='Logging.txt')

                                                # # # # # # # # # # Window Declaration # # # # # # # # # #

class MainWindow(QMainWindow):

    # Window Constructor
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

                                            # # # # # # # # # # Class Variables Initialization # # # # # # # # # #

        self.TimeReadings, self.AmplitudeReadings, self.threadpool = [], [], QThreadPool()
        self.number_of_readings, self.chunkNumber, self.interpolationKind = 1000, 1, 'Polynomial'
        self.prioritizing_constant_number_of_chunks_over_signal_interpolation_coverage, self.isMultipleChunks, self.threadRunning, self.threadPaused = False, False, False, False
        self.signal_curve_fitting_coverage, self.error_map_x_axis_parameter, self.error_map_y_axis_parameter = None, None, None
        self.ui.pauseAndResumeErrorMapPushButton.setEnabled(False); self.ui.numberOfChunksSpinBox.setValue(1)
        self.showAndHideCubicSettings = [ {'UI Element': self.ui.multipleChunksRadioButton,'Function': "show"}, {'UI Element': self.ui.fitPushButton,'Function': "show"}, {'UI Element': self.ui.oneChunkRadioButton,'Function': "show"}, {'UI Element': self.ui.CurveFittingCoveragePrecentageLabel,'Function': "show"}, {'UI Element': self.ui.CurveFittingCoveragePrecentageLcdNumber,'Function': "show"}, {'UI Element': self.ui.signalCoveragePrecentageLabel,'Function': "show"}, {'UI Element': self.ui.extrapolationHorizontalSlider,'Function': "show"}, {'UI Element': self.ui.extrapolationLabel,'Function': "show"}, {'UI Element': self.ui.extrapolationPercentageLabel,'Function': "show"}, {'UI Element': self.ui.precentageOfErrorLabel,'Function': "show"},{'UI Element': self.ui.precentageOfErrorLcdNumber,'Function': "show"}, {'UI Element': self.ui.precentageLabel,'Function': "show"}, {'UI Element': self.ui.fittingOrderLabel,'Function': "hide"}, {'UI Element': self.ui.fittingOrderSpinBox,'Function': "hide"}, {'UI Element': self.ui.numberOfChunksSpinBox,'Function': "hide"}, {'UI Element': self.ui.numberOfChunksLabel,'Function': "hide"}, {'UI Element': self.ui.overlapSpinBox,'Function': "hide"}, {'UI Element': self.ui.overlapLabel,'Function': "hide"}, {'UI Element': self.ui.noOverlappingRadioButton,'Function': "hide"}, {'UI Element': self.ui.overlappingRadioButton,'Function': "hide"}, {'UI Element': self.ui.fullCoverageRadioButton,'Function': "hide"}, {'UI Element': self.ui.constantChunkRadioButton,'Function': "hide"} ]
        self.showAndHidePolynomialAndSplineSettings = [ {'UI Element': self.ui.multipleChunksRadioButton, 'Function': "show"}, {'UI Element': self.ui.fitPushButton, 'Function': "show"}, {'UI Element': self.ui.fittingOrderLabel, 'Function': "show"}, {'UI Element': self.ui.fittingOrderSpinBox, 'Function': "show"}, {'UI Element': self.ui.oneChunkRadioButton, 'Function': "show"}, {'UI Element': self.ui.CurveFittingCoveragePrecentageLabel, 'Function': "show"}, {'UI Element': self.ui.CurveFittingCoveragePrecentageLcdNumber, 'Function': "show"}, {'UI Element': self.ui.signalCoveragePrecentageLabel, 'Function': "show"}, {'UI Element': self.ui.extrapolationHorizontalSlider, 'Function': "show"}, {'UI Element': self.ui.extrapolationLabel, 'Function': "show"}, {'UI Element': self.ui.extrapolationPercentageLabel, 'Function': "show"}, {'UI Element': self.ui.precentageOfErrorLabel, 'Function': "show"}, {'UI Element': self.ui.precentageOfErrorLcdNumber, 'Function': "show"}, {'UI Element': self.ui.precentageLabel, 'Function': "show"}, {'UI Element': self.ui.numberOfChunksLabel, 'Function': "hide"}, {'UI Element': self.ui.numberOfChunksSpinBox, 'Function': "hide"}, {'UI Element': self.ui.overlapSpinBox, 'Function': "hide"},{'UI Element': self.ui.overlapLabel, 'Function': "hide"},{'UI Element': self.ui.noOverlappingRadioButton, 'Function': "hide"}, {'UI Element': self.ui.overlappingRadioButton, 'Function': "hide"}, {'UI Element': self.ui.fullCoverageRadioButton, 'Function': "hide"}, {'UI Element': self.ui.constantChunkRadioButton, 'Function': "hide"} ]
        self.showAndHideAllSettings = [ {'UI Element': self.ui.multipleChunksRadioButton, 'Function': "hide"}, {'UI Element': self.ui.fitPushButton, 'Function': "hide"}, {'UI Element': self.ui.fittingOrderLabel, 'Function': "hide"}, {'UI Element': self.ui.fittingOrderSpinBox, 'Function': "hide"}, {'UI Element': self.ui.oneChunkRadioButton, 'Function': "hide"}, {'UI Element': self.ui.numberOfChunksLabel, 'Function': "hide"}, {'UI Element': self.ui.numberOfChunksSpinBox, 'Function': "hide"}, {'UI Element': self.ui.noOverlappingRadioButton, 'Function': "hide"}, {'UI Element': self.ui.overlapSpinBox, 'Function': "hide"}, {'UI Element': self.ui.overlapLabel, 'Function': "hide"}, {'UI Element': self.ui.fullCoverageRadioButton, 'Function': "hide"}, {'UI Element': self.ui.constantChunkRadioButton, 'Function': "hide"}, {'UI Element': self.ui.CurveFittingCoveragePrecentageLabel, 'Function': "hide"}, {'UI Element': self.ui.CurveFittingCoveragePrecentageLcdNumber, 'Function': "hide"}, {'UI Element': self.ui.extrapolationHorizontalSlider, 'Function': "hide"}, {'UI Element': self.ui.extrapolationLabel, 'Function': "hide"}, {'UI Element': self.ui.extrapolationPercentageLabel, 'Function': "hide"}, {'UI Element': self.ui.precentageOfErrorLabel, 'Function': "hide"}, {'UI Element': self.ui.precentageOfErrorLcdNumber, 'Function': "hide"}, {'UI Element': self.ui.precentageLabel, 'Function': "hide"}, {'UI Element': self.ui.signalCoveragePrecentageLabel, 'Function': "hide"}, {'UI Element': self.ui.errorMapGraphicsView, 'Function': "hide"}, {'UI Element': self.ui.errorMapProgressBar, 'Function': "hide"}, {'UI Element': self.ui.overlappingRadioButton, 'Function': "hide"} ]
        self.overlapSettings, self.chunksNumberSettings = [self.ui.overlapSpinBox, self.ui.overlapLabel, self.ui.fullCoverageRadioButton, self.ui.constantChunkRadioButton], [self.ui.numberOfChunksLabel, self.ui.numberOfChunksSpinBox, self.ui.noOverlappingRadioButton, self.ui.overlappingRadioButton]
        self.errorMapComboBoxesAxesList = [ {'Current Axis Text': 'Choose Axis Parameter', 'Axis List': ["Choose Axis Parameter", "Number of Chunks", "Polynomial Order", "Overlapping Percentage"]}, {'Current Axis Text': 'Polynomial Order', 'Axis List': ["Choose Axis Parameter", "Number of Chunks", "Overlapping Percentage"]}, {'Current Axis Text': 'Number of Chunks', 'Axis List': ["Choose Axis Parameter", "Polynomial Order", "Overlapping Percentage"]}, {'Current Axis Text': 'Overlapping Percentage', 'Axis List': ["Choose Axis Parameter", "Number of Chunks", "Polynomial Order"]} ]
        self.constantParameterSettingDictionaryList = [{'X-Axis': "Number of Chunks", 'Y-Axis': "Polynomial Order", 'Constant Parameter': "Overlapping Percentage", 'Minimum': 0,'Maximum': 25,'Value': 0}, {'X-Axis': "Polynomial Order", 'Y-Axis': "Number of Chunks", 'Constant Parameter': "Overlapping Percentage", 'Minimum': 0,'Maximum': 25,'Value': 0}, {'X-Axis': "Number of Chunks", 'Y-Axis': "Overlapping Percentage", 'Constant Parameter': "Polynomial Order", 'Minimum': 0,'Maximum': 10,'Value': 0}, {'X-Axis': "Overlapping Percentage", 'Y-Axis': "Number of Chunks", 'Constant Parameter': "Polynomial Order", 'Minimum': 0,'Maximum': 10,'Value': 0}, {'X-Axis': "Polynomial Order", 'Y-Axis': "Overlapping Percentage", 'Constant Parameter': "Number of Chunks", 'Minimum': 1,'Maximum': 20,'Value': 1}, {'X-Axis': "Overlapping Percentage", 'Y-Axis': "Polynomial Order", 'Constant Parameter': "Number of Chunks", 'Minimum': 1,'Maximum': 20,'Value': 1}]
        self.spinBoxesInitializationList = [ {'One Chunk Case': True, 'Settings':[(self.ui.overlapSpinBox, 0), (self.ui.numberOfChunksSpinBox, 1)]}, {'One Chunk Case': False, 'Settings':[(self.ui.overlapSpinBox, 0), (self.ui.numberOfChunksSpinBox, 1), (self.ui.fittingOrderSpinBox, 0)]} ]
        self.UIElementsAndFunctions = [ {'UI Element': self.ui.multipleChunksRadioButton.toggled,'Function': self.ChunksNumberRadioButtonsCheck}, {'UI Element': self.ui.oneChunkRadioButton.toggled,'Function': self.ChunksNumberRadioButtonsCheck}, {'UI Element': self.ui.polynomialRadioButton.toggled,'Function': self.InterpolationMethodsRadioButton}, {'UI Element': self.ui.splineRadioButton.toggled,'Function': self.InterpolationMethodsRadioButton}, {'UI Element': self.ui.overlappingRadioButton.toggled,'Function': self.OverlapRadioButtonsCheck}, {'UI Element': self.ui.noOverlappingRadioButton.toggled,'Function': self.OverlapRadioButtonsCheck}, {'UI Element': self.ui.constantChunkRadioButton.toggled,'Function': self.FullFittingCoverageAndConstantChunksNumberSettings}, {'UI Element': self.ui.cubicRadioButton.toggled,'Function': self.InterpolationMethodsRadioButton}, {'UI Element': self.ui.startAndCancelErrorMapPushButton.pressed,'Function': self.StartThreadRunner}, {'UI Element': self.ui.pauseAndResumeErrorMapPushButton.pressed,'Function': self.PauseAndResumeHandler}, {'UI Element': self.ui.openAction.triggered,'Function': self.OpenFile}, {'UI Element': self.ui.fitPushButton.clicked,'Function': self.FitWithUserGivenParameters}, {'UI Element': self.ui.xAxisComboBox.textActivated,'Function': lambda:self.ErrorMapAxesComboBoxesSetter("X-Axis")}, {'UI Element': self.ui.yAxisComboBox.textActivated,'Function': lambda:self.ErrorMapAxesComboBoxesSetter("Y-Axis")}, {'UI Element': self.ui.extrapolationHorizontalSlider.valueChanged,'Function': self.Extrapolation}, {'UI Element': self.ui.fittingOrderSpinBox.valueChanged,'Function': self.ShowChunkEquation}, {'UI Element': self.ui.latexEquationComboBox.currentIndexChanged,'Function': self.ShowChunkEquation}]
        for UIElementDictionary in self.UIElementsAndFunctions:
            UIElementDictionary['UI Element'].connect(UIElementDictionary['Function'])
        self.ui.xAxisComboBox.setCurrentText("Number of Chunks"); self.ErrorMapAxesComboBoxesSetter("X-Axis"); self.ui.yAxisComboBox.setCurrentText("Polynomial Order"); self.ErrorMapAxesComboBoxesSetter("Y-Axis"); self.ShowAndHideManager('all')

                                            # # # # # # # # # # Class Methods Declaration # # # # # # # # # #
    
    # Reading User Opened File
    def OpenFile(self):
        self.file_name = QtWidgets.QFileDialog.getOpenFileName(caption="Choose Signal", directory="", filter="csv (*.csv)")[0]; self.data_frame = pd.read_csv(self.file_name, encoding = 'utf-8').fillna(0)
        self.TimeReadings, self.AmplitudeReadings = self.data_frame.iloc[:,0].to_numpy(), self.data_frame.iloc[:,1].to_numpy()
        self.ui.mainGraphGraphicsView.clear(); self.ui.mainGraphGraphicsView.setYRange(min(self.AmplitudeReadings), max(self.AmplitudeReadings))
        self.ui.mainGraphGraphicsView.plot(self.TimeReadings, self.AmplitudeReadings, pen=pyqtgraph.mkPen('b', width=1.5))
        logging.info('User opening a File')

                                        # # # # # # # # # # Show and Hide UI Elements Functionality # # # # # # # # # #
 
    # Getting User's Selection of Interpolation Method
    def InterpolationMethodsRadioButton(self):
        if self.ui.polynomialRadioButton.isChecked(): self.SetInterpolationMethod('Polynomial')
        elif self.ui.splineRadioButton.isChecked(): self.SetInterpolationMethod('Spline')
        elif self.ui.cubicRadioButton.isChecked(): self.SetInterpolationMethod('Cubic')

    # Handling Interpolation UI Elements According to User's Selection of Interpolation Method
    def SetInterpolationMethod(self, interpolationKind):
        self.interpolationKind = interpolationKind; self.ShowAndHideManager(self.interpolationKind); self.SetInterpolationSpinBoxes(False)

    # Showing and Hiding UI Elements According to User's Selection of Chunks Number Option
    def ChunksNumberRadioButtonsCheck(self):
        if self.ui.multipleChunksRadioButton.isChecked(): self.ui.oneChunkRadioButton.show(); self.isMultipleChunks = True; self.ShowAndHideOverlapOrChunksNumberSettings("show", self.chunksNumberSettings)
        elif self.ui.oneChunkRadioButton.isChecked(): self.SetInterpolationSpinBoxes(True); self.isMultipleChunks = False; self.ShowAndHideOverlapOrChunksNumberSettings("hide", self.overlapSettings); self.ShowAndHideOverlapOrChunksNumberSettings("hide", self.chunksNumberSettings)
        logging.info('Choosing multiple chunks')

    # Showing and Hiding UI Elements According to User's Selection of Overlapping Presence Option
    def OverlapRadioButtonsCheck(self):
        if self.ui.overlappingRadioButton.isChecked(): self.ShowAndHideOverlapOrChunksNumberSettings("show", self.overlapSettings)
        elif self.ui.noOverlappingRadioButton.isChecked(): self.ShowAndHideOverlapOrChunksNumberSettings("hide", self.overlapSettings)
        logging.info('Choosing overlapping')

    # Showing and Hiding Functionality Manager Function According to User's Selection of Chunks Number and Overlapping Presence
    def ShowAndHideOverlapOrChunksNumberSettings(self, displayMethod, overlapOrChunksNumberSettings):
        for overlapOrChunksNumberSettings in overlapOrChunksNumberSettings:
             getattr(overlapOrChunksNumberSettings, displayMethod)()

    # Showing and Hiding Functionality Manager Function According to User's Selection of Interpolation Method
    def ShowAndHideManager(self, shownInterpolationSettings):
        if shownInterpolationSettings == 'Cubic': self.ShowAndHideInterpolationSettings(self.showAndHideCubicSettings)
        elif shownInterpolationSettings == 'Polynomial' or shownInterpolationSettings == 'Spline': self.ShowAndHideInterpolationSettings(self.showAndHidePolynomialAndSplineSettings)
        elif shownInterpolationSettings == 'all': self.ShowAndHideInterpolationSettings(self.showAndHideAllSettings)

    # Showing and Hiding Functionality Worker Function According to User's Selection of Interpolation Method
    def ShowAndHideInterpolationSettings(self, interpoltionSettingsList):
        for Setting in interpoltionSettingsList:
            getattr(Setting['UI Element'], Setting['Function'])()
    
                                        # # # # # # # # # # Miscellaneous Management of UI Elements # # # # # # # # # #

    # Warning User of Consequences of Having Full Fitting Coverage or Keeping Number of Chunks Constant
    def FullFittingCoverageAndConstantChunksNumberSettings(self):
        if self.ui.constantChunkRadioButton.isChecked(): messageBoxElement = QMessageBox.warning(self, 'Warning!', "Signal Curve Fitting Coverage may not be 100%.\nThis applies to Curve Fitting Functionality as well as Error Map Calculation (Polynomial Case)."); self.prioritizing_constant_number_of_chunks_over_signal_interpolation_coverage = True
        elif self.ui.fullCoverageRadioButton.isChecked(): messageBoxElement = QMessageBox.warning(self, 'Warning!', "User Input's Number of Chunks may not be kept Constant.\nThis applies to Curve Fitting Functionality as well as Error Map Calculation (Polynomial Case)."); self.prioritizing_constant_number_of_chunks_over_signal_interpolation_coverage = False
        logging.info('Showing error messages according to overlap settings chosen')

    # Initializing Spinboxes of Interpolation Parameters
    def SetInterpolationSpinBoxes(self, isOneChunkOptionSelected):
        spinBoxSettings = GetDictionaryByKeyValuePair(self.spinBoxesInitializationList, 'One Chunk Case', isOneChunkOptionSelected)
        for spinBox in spinBoxSettings['Settings']:
            spinBox[0].setValue(spinBox[1])

                                            # # # # # # # # # # Curve Fitting Functionality # # # # # # # # # #

    # Managing Chunks' Equation and Starting Curve Fitting Functionlity According to User's Input
    def FitWithUserGivenParameters(self):
        self.ui.mainGraphGraphicsView.clear(); self.ui.mainGraphGraphicsView.plot(self.TimeReadings, self.AmplitudeReadings, pen=pyqtgraph.mkPen('b', width=1.5))
        if self.interpolationKind == 'Polynomial':
            self.ui.latexEquationComboBox.clear()
            for ithIncrement in range(1, self.ui.numberOfChunksSpinBox.value()+1):
                self.ui.latexEquationComboBox.addItem('Chunk '+ str(ithIncrement))
        elif self.interpolationKind == 'Spline':
            if self.ui.fittingOrderSpinBox.value() % 2 == 0 and self.ui.fittingOrderSpinBox.value() != 2 : messageBoxElement = QMessageBox.warning(self, "Error!", 'Spline degree must be odd number or 2 \n Please enter an odd number'); self.ui.fittingOrderSpinBox.setValue(1)
        interpolated_curve_readings, curve_fitting_MSE = self.CurveFitFunctionality(self.ui.numberOfChunksSpinBox.value(),self.ui.overlapSpinBox.value(), self.interpolationKind, self.ui.fittingOrderSpinBox.value(), True)
        self.CurveFittingCoverageCalculation(interpolated_curve_readings); self.ui.precentageOfErrorLcdNumber.display(round(curve_fitting_MSE, 2))

    # Dividing Chunks, Interpolating Each, and Interpolated Curve Readings MSE Calculation
    def CurveFitFunctionality(self, numberOfChuncks, percentageOfOverlapping, InterpolationKind, InterpolationParameter, plot):
        time_chuncks, signal_chuncks = self.DivisionOfSignalIntoChunksWithOrWithoutOverlapping(numberOfChuncks, percentageOfOverlapping)
        curve_fitting_functions = self.IndividualChunksInterpolation(time_chuncks, signal_chuncks, InterpolationKind, InterpolationParameter)
        interpolated_curve_readings, curve_fitting_MSE = self.GeneratingCurveFittingReadingsAndMSE(numberOfChuncks, percentageOfOverlapping, curve_fitting_functions, time_chuncks, plot)
        return interpolated_curve_readings, curve_fitting_MSE

    # Calculating Curve Fitting Coverage According to User's Inputs and Overlap Settings
    def CurveFittingCoverageCalculation(self, interpolated_curve_readings):
        self.signal_curve_fitting_coverage = round( (len(interpolated_curve_readings) / self.number_of_readings) * 100 )
        self.ui.CurveFittingCoveragePrecentageLcdNumber.display(self.signal_curve_fitting_coverage)

    # Deriving Parameters Needed for Interpolation from User Given Parameters
    def DerivedSignalParametersCalculation(self, numberOfChuncks, percentageOfOverlapping):
        percentageOfOverlapping, chunck_size = round(percentageOfOverlapping/100, 2), round( self.number_of_readings/numberOfChuncks ); overlapping_range = round( (self.number_of_readings/numberOfChuncks)*percentageOfOverlapping )
        return chunck_size, overlapping_range

    # Dividing Chunks Functionality Taking Overlapping in Consideration
    def DivisionOfSignalIntoChunksWithOrWithoutOverlapping(self, numberOfChuncks, percentageOfOverlapping):
        chunck_size, overlapping_range = self.DerivedSignalParametersCalculation(numberOfChuncks, percentageOfOverlapping)
        time_chuncks = [ self.TimeReadings[i:i+chunck_size] for i in range(0, self.number_of_readings - overlapping_range, chunck_size - overlapping_range) ]; signal_chuncks = [ self.AmplitudeReadings[i:i+chunck_size] for i in range(0, self.number_of_readings - overlapping_range, chunck_size - overlapping_range) ]
        if overlapping_range != 0 and self.prioritizing_constant_number_of_chunks_over_signal_interpolation_coverage: time_chuncks = [ time_chuncks[i] for i in range(numberOfChuncks) ]; signal_chuncks = [ signal_chuncks[i] for i in range(numberOfChuncks) ]
        return time_chuncks, signal_chuncks

    # Generating Interpolation Functions for Each Chunk
    def IndividualChunksInterpolation(self, time_chuncks, signal_chuncks, interpolation_kind, interpolation_parameter):
        if interpolation_kind == 'Polynomial': curve_fitting_functions = [ np.poly1d(np.polyfit(time_chuncks[i], signal_chuncks[i], interpolation_parameter)) for i in range(len(time_chuncks)) ]
        elif interpolation_kind == 'Spline': curve_fitting_functions = [ (make_interp_spline(time_chuncks[i], signal_chuncks[i], k=interpolation_parameter)) for i in range(len(time_chuncks))]
        elif interpolation_kind == 'Cubic': curve_fitting_functions = [ (interp1d(time_chuncks[i], signal_chuncks[i], kind='cubic')) for i in range(len(time_chuncks))]
        return curve_fitting_functions

    # Substituing in Chunks' Interpolation Functions and Averaging Overlapped Regions
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

                                            # # # # # # # # # # Extrapolation Functionality # # # # # # # # # #

    # Extrapolating Ratio of Signal's End based on Rest of Signal
    def Extrapolation(self):
        self.extrapolationSliderValue = self.ui.extrapolationHorizontalSlider.value()
        self.ui.extrapolationPercentageLabel.setText(f'{self.extrapolationSliderValue}% Original Signal')
        self.lastSignalIndex= int((self.extrapolationSliderValue/100)* len(self.TimeReadings))
        self.fittingOrder, signalAmplitude, signalTime, residualTime, extrapolatedAmplitude = self.ui.fittingOrderSpinBox.value(), [], [], [], []
        signalTime, signalAmplitude, residualTime = self.TimeReadings[0:self.lastSignalIndex], self.AmplitudeReadings[0:self.lastSignalIndex], self.TimeReadings[self.lastSignalIndex:len(self.TimeReadings)]     
        self.equationCoefficients = np.polyfit(signalTime, signalAmplitude, self.fittingOrder); self.poly1d_fn, extrapolatedAmplitude = np.poly1d(self.equationCoefficients ), np.polyval(self.equationCoefficients , residualTime)  
        self.ui.mainGraphGraphicsView.clear(); self.ui.mainGraphGraphicsView.plot(self.TimeReadings, self.AmplitudeReadings, pen=pyqtgraph.mkPen('b', width=1.5))
        self.ui.mainGraphGraphicsView.plot(signalTime, self.poly1d_fn(signalTime), pen=pyqtgraph.mkPen('g', width=1.5, style = QtCore.Qt.DotLine)); self.ui.mainGraphGraphicsView.plot(residualTime, extrapolatedAmplitude, pen=pyqtgraph.mkPen('r', width=1.5, style = QtCore.Qt.DotLine))
        logging.info('Using the extrapolation slider')

                                                # # # # # # # # # # Error Map Settings # # # # # # # # # #

    # Managing User's Choice of Error Map Axes
    def ErrorMapAxesComboBoxesSetter(self, axisType):
        if axisType == "X-Axis": self.ErrorMapAxesComboBoxesHelperFunction(self.ui.xAxisComboBox, self.ui.yAxisComboBox)
        elif axisType == "Y-Axis": self.ErrorMapAxesComboBoxesHelperFunction(self.ui.yAxisComboBox, self.ui.xAxisComboBox)
        logging.info('Choosing axes for the error map')

    # User's Choice of Error Map Axes Worker Function
    def ErrorMapAxesComboBoxesHelperFunction(self, currentAxisComboBox, otherAxisComboBox):
        otherAxisText, currentAxisText = otherAxisComboBox.currentText(), currentAxisComboBox.currentText()
        comboBoxAxisList = GetDictionaryByKeyValuePair(self.errorMapComboBoxesAxesList, 'Current Axis Text', currentAxisText)
        otherAxisComboBox.clear(); otherAxisComboBox.addItems(comboBoxAxisList["Axis List"]); otherAxisComboBox.setCurrentText(otherAxisText); self.ConstantParameterSetting()

    # Setting Third Constant of Error Map Calculation According to User's Selection of Error Map Axes
    def ConstantParameterSetting(self):
        if self.ui.xAxisComboBox.currentText() != 'Choose Axis Parameter' and self.ui.yAxisComboBox.currentText() != 'Choose Axis Parameter':
            xAxisCurrentText, yAxisCurrentText = self.ui.xAxisComboBox.currentText(), self.ui.yAxisComboBox.currentText()
            constantParameter = GetDictionaryByTwoKeyValuePairs(self.constantParameterSettingDictionaryList, 'X-Axis', xAxisCurrentText, 'Y-Axis', yAxisCurrentText)
            self.ui.constantParameterLabel.setText(constantParameter['Constant Parameter']); self.ui.constantParameterSpinBox.setMinimum(constantParameter['Minimum']); self.ui.constantParameterSpinBox.setMaximum(constantParameter['Maximum']); self.ui.constantParameterSpinBox.setValue(constantParameter['Value'])

                                            # # # # # # # # # # Error Map Functionality # # # # # # # # # #

    # Connecting Error Map Progress Signal to UI Progress Bar
    def ReportProgress(self, progressValue): self.ui.errorMapProgressBar.setValue(progressValue)

    # Clearing Old Error Map and Starting New One
    def ClearErrorMap(self):
        self.errorMapfigure = plt.figure(figsize=(15,5)); self.errorMapAxes = self.errorMapfigure.get_axes()
        self.Canvas = FigureCanvas(self.errorMapfigure); self.ui.errorMapGridLayout.addWidget(self.Canvas,0, 0, 1, 1)

    # Managing UI Elements According to Start and End of Error Map
    def ErrorMapStartAndEndSettings(self, threadRunningValue, startAndCancelErrorMapButtonText, pauseAndResumeErrorMapButtonDisplay):
        self.threadRunning = threadRunningValue; self.ui.startAndCancelErrorMapPushButton.setText(startAndCancelErrorMapButtonText)
        self.ui.pauseAndResumeErrorMapPushButton.setEnabled(pauseAndResumeErrorMapButtonDisplay); self.ui.errorMapProgressBar.setValue(0)
        logging.info('Error map progress bar')

    # Managing UI Elements According to Pause and Resume of Error Map
    def ErrorMapPauseAndResumeSettings(self, threadPausedValue, mode, pauseAndResumeErrorMapButtonText):
        self.threadPaused = threadPausedValue; self.errorMapWorker.PauseAndResume(mode)
        self.ui.pauseAndResumeErrorMapPushButton.setText(pauseAndResumeErrorMapButtonText)

    # Start Running of Thread Containing Error Map Worker
    def StartThreadRunner(self):
        if not self.threadRunning:
            self.errorMapWorker = ErrorMapWorker(self, self.ui.xAxisComboBox.currentText(), self.ui.yAxisComboBox.currentText(), self.ui.constantParameterSpinBox.value()); self.threadPaused = False
            self.errorMapWorkerSignalSettings = [{'Signal': self.errorMapWorker.ErrorMapWorkerSignals.ErrorMapProgressSignal, 'Function': self.ReportProgress}, {'Signal':self.errorMapWorker.ErrorMapWorkerSignals.ErrorMapStartedSignal, 'Function': self.StartErrorMap}, {'Signal':self.errorMapWorker.ErrorMapWorkerSignals.ErrorMapFinishedSignal, 'Function': self.FinishErrorMap}]
            for errorMapWorkerSignalSetting in self.errorMapWorkerSignalSettings:
                errorMapWorkerSignalSetting['Signal'].connect(errorMapWorkerSignalSetting['Function'])
            self.threadpool.start(self.errorMapWorker)
        else: self.errorMapWorker.stop(); self.ErrorMapStartAndEndSettings(False, 'Start', False)

    # Showing Error Map After Finish of Error Map Worker
    def FinishErrorMap(self):
        self.ErrorMapStartAndEndSettings(False, 'Start', False); self.ClearErrorMap()
        self.errorMapAxes = sns.heatmap(self.errorMapWorker.errors_matrix, cmap="Spectral_r")
        self.errorMapAxes.set_title("Curve Fitting Percentage Error Map"); self.errorMapAxes.set_xticks(range(self.errorMapWorker.x_axis_parameter_dictionary['Full Range'])); self.errorMapAxes.set_yticks(range(self.errorMapWorker.y_axis_parameter_dictionary['Full Range']))
        self.errorMapAxes.set_xticklabels( list( np.arange(self.errorMapWorker.x_axis_parameter_dictionary['Start Range'], self.errorMapWorker.x_axis_parameter_dictionary['End Range']+1 ) ) ); self.errorMapAxes.set_yticklabels( list( np.arange(self.errorMapWorker.y_axis_parameter_dictionary['End Range'], self.errorMapWorker.y_axis_parameter_dictionary['Start Range']-1, -1 ) ) )
        self.errorMapAxes.set( xlabel = self.errorMapWorker.x_axis_parameter_dictionary['Parameter Name'], ylabel = self.errorMapWorker.y_axis_parameter_dictionary['Parameter Name'] ); self.Canvas.draw()
        errorMapSpacer = QtWidgets.QSpacerItem(550, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum); self.ui.errorMapGridLayout.addItem(errorMapSpacer, 1, 0, 1, 1)
        
    # Calling Error Map Worker to Start Calculating Error Map
    def StartErrorMap(self):
        self.ErrorMapStartAndEndSettings(True, 'Cancel', True); self.ui.errorMapProgressBar.show()
        logging.info('Start error map')

    # According to Error Map's State of Pause or Resume, UI Elements Settings are Managed
    def PauseAndResumeHandler(self):
        if not self.threadPaused: self.ErrorMapPauseAndResumeSettings(True, 'Pause', 'Resume')
        else: self.ErrorMapPauseAndResumeSettings(False, 'Resume', 'Pause')

                                            # # # # # # # # # # Chunks' Equation Functionality # # # # # # # # # #
    
    # Calculating Coefficients of Interpolation Method
    def GetChunkEquationCoefficients(self, chunkNumber):
        coefficientsCount, self.chunckSize, self.fittingOrder = 0, ceil(1000/self.ui.numberOfChunksSpinBox.value()), self.ui.fittingOrderSpinBox.value()
        for ithIncrement in range(0, len(self.TimeReadings)-1,self.chunckSize):
            signalAmplitude, signalTime, coefficientsIncrement = [], [], ithIncrement; coefficientsCount +=1
            for jthIncrement in range(self.chunckSize-1):
                if coefficientsIncrement < len(self.TimeReadings): signalAmplitude.append(self.AmplitudeReadings[coefficientsIncrement]); signalTime.append(self.TimeReadings[coefficientsIncrement]); coefficientsIncrement += 1
            self.equationCoefficients  = np.polyfit(signalTime[0:int(self.chunckSize-1)], signalAmplitude[0:int(self.chunckSize-1)],self.fittingOrder)
            if coefficientsCount == chunkNumber: return self.equationCoefficients 
        logging.info('Showing each chunk equation')

    # Rendering Equation in Latex Format
    def RenderLatexEquation(self, formula, fontsize=12, dpi=300, format_='svg'):
        equationFigure = plt.figure(figsize=(0.01, 0.01)); equationFigure.text(0, 0, u'${}$'.format(formula), color='black',fontsize=fontsize)
        buffer_ = BytesIO(); equationFigure.savefig(buffer_, dpi=dpi, transparent=True, format=format_, bbox_inches='tight', pad_inches=0.0)
        plt.close(equationFigure); return buffer_.getvalue()

    # Showing Chunks Equation in Appropriate Place and Format
    def ShowChunkEquation(self):
        global fittingDegree
        if self.isMultipleChunks == False:
            fittingDegree, equationCoefficients = self.ui.fittingOrderSpinBox.value(), np.polyfit(self.TimeReadings, self.AmplitudeReadings, fittingDegree); reversedCoefficients, xSymbols = equationCoefficients[::-1], symbols("x")
            equation_format = sum(S("{:6.2f}".format(jthCoefficient))*xSymbols**ithCoefficient for ithCoefficient, jthCoefficient in enumerate(reversedCoefficients[::1])); latex_equation = printing.latex(equation_format)     
            image_bytes = self.RenderLatexEquation(latex_equation, fontsize=7, dpi=200, format_='png'); Qpixmap = QPixmap(); Qpixmap .loadFromData(image_bytes); self.ui.latexEquationLabel.setPixmap(Qpixmap )
        elif self.isMultipleChunks == True:
            self.chunkNumber, reversedCoefficients = self.ui.latexEquationComboBox.currentIndex() + 1, self.GetChunkEquationCoefficients(self.chunkNumber)
            fittingDegree, xSymbols = self.ui.fittingOrderSpinBox.value(), symbols("x"); equation_format = sum(S("{:6.2f}".format(jthCoefficient))*xSymbols**ithCoefficient for ithCoefficient, jthCoefficient in enumerate(reversedCoefficients[::1]))
            latex_equation = printing.latex(equation_format); image_bytes = self.RenderLatexEquation(latex_equation, fontsize=7, dpi=200, format_='png'); Qpixmap  = QPixmap(); Qpixmap .loadFromData(image_bytes); self.ui.latexEquationLabel.setPixmap(Qpixmap )
        logging.info('Show interpolation equation')
        
                                                # # # # # # # # # # General Functions # # # # # # # # # #

# Find Dictionary with Matching Two Key Value Pairs
def GetDictionaryByTwoKeyValuePairs(dictionaries_list, first_key_to_search_by, first_value_to_search_by, second_key_to_search_by, second_value_to_search_by):
        dictionary_to_find = {}
        for dictionary in dictionaries_list:
            if dictionary[first_key_to_search_by] == first_value_to_search_by and dictionary[second_key_to_search_by] == second_value_to_search_by: dictionary_to_find = dictionary
        return dictionary_to_find
    
                                                    # # # # # # # # # # Execution  # # # # # # # # # #
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())