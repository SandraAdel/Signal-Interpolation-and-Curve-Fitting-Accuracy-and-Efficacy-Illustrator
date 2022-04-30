import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import pyqtgraph
from pyqtgraph import PlotWidget
import pandas as pd
import numpy as np
from sympy import rad
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
        self.oneChunck = 0
        self.result = []

        # Hide error map elements
        self.ui.errorMapGraphicsView.hide()
        self.ui.errorLabel.hide()
        self.ui.errorMapProgressBar.hide()
        # Hide polynomial controls 
        self.ui.polynomialFitPushButton.hide()
        self.ui.polynomialFittingOrderLabel.hide()
        self.ui.polynomialFittingOrderSpinBox.hide()
        self.ui.polynomialNumberOfChuncksLabel.hide()
        self.ui.polynomialNumberOfChuncksSpinBox.hide()
        self.ui.polynomialOerlapSpinBox.hide()
        self.ui.polynomialOverlapLabel.hide()
        self.ui.polynomialOneChunckRadioButton.hide()
        self.ui.polynomialMultipleChuncksRadioButton.hide()
        
        # Links of GUI Elements to Methods:
        self.ui.openAction.triggered.connect(lambda: self.OpenFile())
        self.ui.interpolationMethodComboBox.currentIndexChanged.connect(lambda: self.interpolatioMethodes(self.ui.interpolationMethodComboBox.currentIndex()))
        self.ui.polynomialMultipleChuncksRadioButton.toggled.connect(lambda: self.radioButtonMultiple())
        self.ui.polynomialOneChunckRadioButton.toggled.connect(lambda: self.radioButton())
        self.ui.polynomialFitPushButton.clicked.connect(lambda: self.interpolation())


    # Methods
    def OpenFile(self):
        self.file_name = QtWidgets.QFileDialog.getOpenFileName(caption="Choose Signal", directory="", filter="csv (*.csv)")[0]
        self.data_frame = pd.read_csv(self.file_name, encoding = 'utf-8').fillna(0)
        self.TimeReadings = self.data_frame.iloc[:,0].to_numpy()
        self.AmplitudeReadings = self.data_frame.iloc[:,1].to_numpy()
        self.ui.mainGraphGraphicsView.plot(self.TimeReadings, self.AmplitudeReadings, pen=pyqtgraph.mkPen('b', width=1.5))
    
    def interpolatioMethodes(self, index):
        if index == 0:
            self.ui.polynomialOneChunckRadioButton.show()
            self.ui.polynomialMultipleChuncksRadioButton.show()
            self.ui.polynomialFitPushButton.show()
            self.ui.polynomialFittingOrderLabel.show()
            self.ui.polynomialFittingOrderSpinBox.show()
            
    #! COODE REPETITION TACK CAAAAAAAAAAAAAAARE        
    def radioButtonMultiple (self):
        if self.ui.polynomialMultipleChuncksRadioButton.isChecked():
            self.ui.polynomialNumberOfChuncksLabel.show()
            self.ui.polynomialNumberOfChuncksSpinBox.show()
            self.ui.polynomialOerlapSpinBox.show()
            self.ui.polynomialOverlapLabel.show()


    def radioButton (self):
        if self.ui.polynomialOneChunckRadioButton.isChecked():
            self.oneChunck = 1
            self.ui.polynomialNumberOfChuncksLabel.hide()
            self.ui.polynomialNumberOfChuncksSpinBox.hide()
            self.ui.polynomialOerlapSpinBox.hide()
            self.ui.polynomialOverlapLabel.hide()



    def interpolation (self):
            self.order = self.ui.polynomialFittingOrderSpinBox.value()
            self.coeff = np.polyfit(self.TimeReadings, self.AmplitudeReadings,self.order)
            self.poly1d_fn = np.poly1d(self.coeff) 
            self.ui.mainGraphGraphicsView.clear() 
            self.ui.mainGraphGraphicsView.plot(self.TimeReadings, self.AmplitudeReadings, pen=pyqtgraph.mkPen('b', width=1.5))
            self.ui.mainGraphGraphicsView.plot(self.TimeReadings, self.poly1d_fn(self.TimeReadings), pen=pyqtgraph.mkPen('g', width=1.5, style = QtCore.Qt.DotLine))

    


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())