                                                        # # # # # # # # # # Imports # # # # # # # # # # 

import time; import numpy as np; from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QRunnable


                                                    # # # # # # # # # # Classes Declaration # # # # # # # # # # 
# Defining Error Map Signals
class ErrorMapWorkerSignals(QObject):
    ErrorMapStartedSignal, ErrorMapFinishedSignal, ErrorMapProgressSignal = pyqtSignal(), pyqtSignal(), pyqtSignal(int)

# Defining Error Map Worker to be Put in Thread
class ErrorMapWorker(QRunnable):
    ErrorMapWorkerSignals = ErrorMapWorkerSignals()

    # Error Map Worker Constructor
    def __init__(self, window_object, x_axis_parameter, y_axis_parameter, constant_parameter_value):
        super().__init__()
        self.isErrorMapPaused, self.isErrorMapStopped, self.window_object, self.errors_matrix, self.x_axis_parameter_dictionary, self.y_axis_parameter_dictionary = False, False, window_object, None, None, None
        self.curve_fitting_parameters_list = [ {'Parameter Name': 'Number of Chunks', 'Start Range': 1, 'End Range': 20, 'Full Range': 20}, {'Parameter Name': 'Overlapping Percentage', 'Start Range': 0, 'End Range': 25, 'Full Range':26}, {'Parameter Name': 'Polynomial Order', 'Start Range': 0, 'End Range': 10, 'Full Range': 11} ]
        self.x_axis_parameter, self.y_axis_parameter, self.constant_parameter_value = x_axis_parameter, y_axis_parameter, constant_parameter_value

    # Assigning Start and End Range of Error Map Calculation Parameters
    def AssignLoopingRangeForCurveFittingParameters(self, dictionary_of_curve_fitting_parameter_to_assign, x_axis_parameter, y_axis_parameter, constant_parameter_value):
        if x_axis_parameter == dictionary_of_curve_fitting_parameter_to_assign['Parameter Name'] or y_axis_parameter == dictionary_of_curve_fitting_parameter_to_assign['Parameter Name']: return (dictionary_of_curve_fitting_parameter_to_assign['Start Range'], dictionary_of_curve_fitting_parameter_to_assign['End Range'])
        else: return (constant_parameter_value, constant_parameter_value)

    # Error Map Calculation and Formation
    @pyqtSlot()
    def run(self):

        self.ErrorMapWorkerSignals.ErrorMapStartedSignal.emit()
        self.x_axis_parameter_dictionary, self.y_axis_parameter_dictionary = GetDictionaryByKeyValuePair(self.curve_fitting_parameters_list, 'Parameter Name', self.x_axis_parameter), GetDictionaryByKeyValuePair(self.curve_fitting_parameters_list, 'Parameter Name', self.y_axis_parameter)
        number_of_chunks_range_on_error_map, overlapping_percentage_range_on_error_map, polynomial_order_range_on_error_map = self.AssignLoopingRangeForCurveFittingParameters( GetDictionaryByKeyValuePair(self.curve_fitting_parameters_list, 'Parameter Name', 'Number of Chunks'), self.x_axis_parameter, self.y_axis_parameter, self.constant_parameter_value ), self.AssignLoopingRangeForCurveFittingParameters( GetDictionaryByKeyValuePair(self.curve_fitting_parameters_list, 'Parameter Name', 'Overlapping Percentage'), self.x_axis_parameter, self.y_axis_parameter, self.constant_parameter_value ), self.AssignLoopingRangeForCurveFittingParameters( GetDictionaryByKeyValuePair(self.curve_fitting_parameters_list, 'Parameter Name', 'Polynomial Order'), self.x_axis_parameter, self.y_axis_parameter, self.constant_parameter_value )
        self.errors_matrix, self.row_index, self.column_index = np.zeros(( self.y_axis_parameter_dictionary['Full Range'] , self.x_axis_parameter_dictionary['Full Range'] )), self.y_axis_parameter_dictionary['Full Range'] - 1, 0; current_progress, progress_step = 0, 100/(self.errors_matrix.size)

        for overlapping_percentage in range(overlapping_percentage_range_on_error_map[0], overlapping_percentage_range_on_error_map[1]+1):
            for polynomial_order in range(polynomial_order_range_on_error_map[0], polynomial_order_range_on_error_map[1]+1):
                for number_of_chunks in range(number_of_chunks_range_on_error_map[0], number_of_chunks_range_on_error_map[1]+1):

                    __ , MSE_error = self.window_object.CurveFitFunctionality(number_of_chunks, overlapping_percentage, 'Polynomial', polynomial_order, False)
                    self.errors_matrix[ self.row_index, self.column_index ] = MSE_error; current_progress += progress_step
                    self.ErrorMapWorkerSignals.ErrorMapProgressSignal.emit(round(current_progress)); time.sleep(0.01)                   
                    while self.isErrorMapPaused: time.sleep(0)
                    if self.isErrorMapStopped: return

                    self.RowOrColumnMatrixIndicesIncrement('Number of Chunks', True, True, self.row_index, self.column_index+1, self.row_index-1, self.column_index)
                self.RowOrColumnMatrixIndicesIncrement('Number of Chunks', True, True, self.row_index-1, 0, self.y_axis_parameter_dictionary['Full Range'] - 1, self.column_index+1)
                self.RowOrColumnMatrixIndicesIncrement('Polynomial Order', self.y_axis_parameter != 'Number of Chunks', self.x_axis_parameter != 'Number of Chunks', self.row_index, self.column_index+1, self.row_index-1, self.column_index)
            self.RowOrColumnMatrixIndicesIncrement('Polynomial Order', True, True, self.row_index-1, 0, self.y_axis_parameter_dictionary['Full Range'] - 1, self.column_index+1)
        self.ErrorMapWorkerSignals.ErrorMapFinishedSignal.emit()

    # Handler for Pausing and Resuming Error Map Calculation and Formation
    def PauseAndResume(self, order):
        if order == 'Pause': self.isErrorMapPaused = True
        elif order == 'Resume': self.isErrorMapPaused = False

    # Handler for Error Map Cancellation
    def stop(self): self.isErrorMapStopped = True

    # Incrementing Row and Column Indices of Next Error Value in Error Map
    def RowOrColumnMatrixIndicesIncrement(self, parameterToCheck, secondIfCondition, secondElseCondition, ifConditionRowValue, ifConditionColumnValue, elseConditionRowValue, elseConditionColumnValue):
        if self.x_axis_parameter == parameterToCheck and secondIfCondition: self.row_index = ifConditionRowValue; self.column_index = ifConditionColumnValue
        elif self.y_axis_parameter == parameterToCheck and secondElseCondition: self.row_index = elseConditionRowValue; self.column_index = elseConditionColumnValue

                                                    # # # # # # # # # # General Functions # # # # # # # # # # 
# Find Dictionary with Matching Key Value Pair
def GetDictionaryByKeyValuePair(dictionaries_list, key_to_search_by, value_to_search_by):
        dictionary_to_find = {}
        for dictionary in dictionaries_list:
            if dictionary[key_to_search_by] == value_to_search_by: dictionary_to_find = dictionary
        return dictionary_to_find