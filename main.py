import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import pyqtgraph
from pyqtgraph import PlotWidget
import pandas as pd
from GUI import Ui_MainWindow


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Variables Initialization
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

    # Methods

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())