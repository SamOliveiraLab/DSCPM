import matplotlib.dates as mdates
import numpy as np
import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QGridLayout
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd
import datetime
from serial_communication import communication as comm


class ArduinoGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.data = pd.DataFrame(
            columns=['datetime', 'set_active', 'flowrate', 'direction'])

    def initUI(self):
        self.setWindowTitle('Arduino Flow Rate Controller')

        self.layout = QGridLayout()

        # Top Left: User Input
        self.flowRateLabel = QLabel('Flow Rate (µL/min):')
        self.flowRateInput = QLineEdit()
        self.flowRateInput.setPlaceholderText(
            'Enter flow rate (0.00 - 500.00 µL/min)')

        self.directionLabel = QLabel('Direction:')
        self.directionInput = QComboBox()
        self.directionInput.addItems(['Forward', 'Reverse'])

        self.setButton = QPushButton('Set')
        self.setButton.clicked.connect(self.setValues)

        self.topLeftLayout = QVBoxLayout()
        self.topLeftLayout.addWidget(self.flowRateLabel)
        self.topLeftLayout.addWidget(self.flowRateInput)
        self.topLeftLayout.addWidget(self.directionLabel)
        self.topLeftLayout.addWidget(self.directionInput)
        self.topLeftLayout.addWidget(self.setButton)

        self.layout.addLayout(self.topLeftLayout, 0, 0)

        # Top Right: Current Readout
        self.currentFlowRateLabel = QLabel('Current Flow Rate (µL/min):')
        self.currentFlowRateDisplay = QLineEdit()
        self.currentFlowRateDisplay.setReadOnly(True)

        self.currentDirectionLabel = QLabel('Current Direction:')
        self.currentDirectionDisplay = QLineEdit()
        self.currentDirectionDisplay.setReadOnly(True)

        self.updateButton = QPushButton('Update')
        self.updateButton.clicked.connect(self.updateValues)

        self.topRightLayout = QVBoxLayout()
        self.topRightLayout.addWidget(self.currentFlowRateLabel)
        self.topRightLayout.addWidget(self.currentFlowRateDisplay)
        self.topRightLayout.addWidget(self.currentDirectionLabel)
        self.topRightLayout.addWidget(self.currentDirectionDisplay)
        self.topRightLayout.addWidget(self.updateButton)

        self.layout.addLayout(self.topRightLayout, 0, 1)

        # Bottom: Plot
        self.plotWidget = PlotCanvas(self, width=10, height=5)
        self.layout.addWidget(self.plotWidget, 1, 0, 1, 2)

        # Set layout
        self.setLayout(self.layout)

    def setValues(self):
        try:
            flowrate = float(self.flowRateInput.text())
            if flowrate < 0 or flowrate > 500:
                raise ValueError
        except ValueError:
            self.flowRateInput.setText('')
            return

        direction = self.directionInput.currentText()
        flowrate = flowrate * (-1 if direction == 'Reverse' else 1)
        comm.communicate(flowrate)
        self.updateValues(data=flowrate)

    def updateValues(self, data=None):
        # Call the communicate function with None to get the current values
        comm.communicate(data)

        # Dynamically construct the path to pump_log.csv
        base_dir = os.path.dirname(os.path.abspath(
            __file__))  # Get the directory of app.py
        file_path = os.path.join(
            base_dir, '../pump_log.csv')

        try:
            data = pd.read_csv(file_path)
            if data.empty or 'actual_rate' not in data.columns or 'set_rate' not in data.columns:
                raise ValueError(
                    "CSV file is empty or missing required columns")

            self.plotWidget.update_plot(data)
        except (FileNotFoundError, ValueError) as e:
            print(f"Error reading the file: {e}")
            return

        # Update the GUI with the current values
        response = data.iloc[-1]
        actual_fl = float(response['actual_rate'])
        def sign(x): return 'Forward' if x > 0 else 'Reverse'
        self.currentFlowRateDisplay.setText(f'{abs(actual_fl)} µL/min')
        self.currentDirectionDisplay.setText(sign(actual_fl))


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=10, height=5, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)
        self.setParent(parent)
        self.plot()

    def plot(self):
        self.axes.clear()
        self.axes.set_title('Flow Rate History')
        self.axes.set_xlabel('Time')
        self.axes.set_ylabel('Flow Rate (µL/min)')
        self.draw()


def setValues(self):
    try:
        flowrate = float(self.flowRateInput.text())
        if flowrate < 0 or flowrate > 500:
            raise ValueError
    except ValueError:
        self.flowRateInput.setText('')
        return

    direction = self.directionInput.currentText()
    flowrate = flowrate * (-1 if direction == 'Reverse' else 1)
    comm.communicate(flowrate)
    self.data = self.data._append({'datetime': datetime.datetime.now(
    ), 'set_active': True, 'flowrate': flowrate, 'direction': direction}, ignore_index=True)


def updateValues(self):
    # Call the communicate function with None to get the current values
    comm.communicate(None)

    # Dynamically construct the path to pump_log.csv
    base_dir = os.path.dirname(os.path.abspath(
        __file__))  # Get the directory of app.py
    file_path = os.path.join(
        base_dir, '../pump_log.csv')

    try:
        data = pd.read_csv(file_path)
        if data.empty or 'actual_rate' not in data.columns or 'set_rate' not in data.columns:
            raise ValueError(
                "CSV file is empty or missing required columns")

        self.plotWidget.update_plot(data)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error reading the file: {e}")
        return

    # Update the GUI with the current values
    response = data.iloc[-1]
    actual_fl = float(response['actual_rate'])
    def sign(x): return 'Forward' if x > 0 else 'Reverse'
    self.currentFlowRateDisplay.setText(f'{actual_fl} µL/min')
    self.currentDirectionDisplay.setText(sign(actual_fl))


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=10, height=5, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)
        self.setParent(parent)
        self.plot()

    def plot(self):
        self.axes.clear()
        self.axes.set_title('Flow Rate History')
        self.axes.set_xlabel('Time')
        self.axes.set_ylabel('Flow Rate (µL/min)')
        self.draw()

    def update_plot(self, data):
        """
        Updates the plot with flow rate history using self.axes, dynamically scaling the x-axis
        and handling None/NaN values.
        """
        if data is None:
            print("No data to plot.")
            return

        try:
            # Print loaded data for debugging
            # print("Loaded Data:\n", data)

            # Safely convert columns and handle NaN values
            # Ensure datetime conversion
            time = pd.to_datetime(data['datetime'], errors='coerce')
            # Coerce invalid entries to NaN
            set_data = pd.to_numeric(data['set_rate'], errors='coerce')
            # Coerce invalid entries to NaN
            actual_data = pd.to_numeric(data['actual_rate'], errors='coerce')

            # Drop NaN values for each series individually
            valid_set_mask = ~set_data.isna()
            valid_actual_mask = ~actual_data.isna()

            filtered_time_set = time[valid_set_mask]
            filtered_set_data = set_data[valid_set_mask]
            filtered_time_actual = time[valid_actual_mask]
            filtered_actual_data = actual_data[valid_actual_mask]

            # Check if filtered data is empty to prevent plotting issues
            if filtered_time_set.empty or filtered_time_actual.empty:
                print("No valid data to plot.")
                return

            # Clear the plot and set titles and labels
            self.axes.clear()
            self.axes.set_title('Flow Rate History', fontsize=14)
            self.axes.set_xlabel('Time', fontsize=12)
            self.axes.set_ylabel('Flow Rate (µL/min)', fontsize=12)

            # Plot filtered data
            self.axes.plot(
                filtered_time_set, filtered_set_data,
                label='Set Flow Rate', color='blue', marker='o', linestyle='-'
            )
            self.axes.plot(
                filtered_time_actual, filtered_actual_data,
                label='Actual Flow Rate', color='red', marker='x', linestyle='-'
            )

            # Format the x-axis for datetime
            self.axes.xaxis.set_major_formatter(
                mdates.DateFormatter('%H:%M:%S'))
            self.axes.xaxis.set_major_locator(mdates.AutoDateLocator())
            self.axes.tick_params(axis='x', rotation=25)

            # Add legend and grid for better readability
            self.axes.legend(loc='upper right', fontsize=10)
            self.axes.grid(True, linestyle='--', alpha=0.5)

            # Redraw the canvas
            self.draw()

        except Exception as e:
            print(f"Error during plotting: {e}")
            return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = ArduinoGUI()
    gui.show()
    sys.exit(app.exec_())
