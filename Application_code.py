
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtWidgets
from pyfirmata2 import Arduino
from scipy import signal
from iir_filter import IIR_filter  # Ensure this is correctly implemented


# Initialize filter coefficients
sos = signal.butter(4, [14/300*2, 20/300*2], 'bandpass', output='sos')

class QtPanningPlot:
    def __init__(self, layout, title, filter_enabled=False):
        self.pw = pg.PlotWidget()
        layout.addWidget(self.pw)
        self.pw.setYRange(-1, 1)
        self.pw.setXRange(0, 500 / samplingRate)
        self.plt = self.pw.plot()
        self.data = []
        self.filtered_data = []
        self.filter_enabled = filter_enabled
        if self.filter_enabled:
            self.iir_filter = IIR_filter(sos)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(100)

    def update(self):
        self.data = self.data[-500:]
        self.filtered_data = self.filtered_data[-500:]
        if self.data:
            x = np.linspace(0, len(self.data) / samplingRate, len(self.data))
            self.plt.setData(x=x, y=self.data if not self.filter_enabled else self.filtered_data)

    def addData(self, d):
        self.data.append(d)
        if self.filter_enabled:
            filtered_sample = self.iir_filter.filter(d)
            self.filtered_data.append(filtered_sample)


app = pg.mkQApp()
mw = QtWidgets.QMainWindow()
mw.setWindowTitle('Real-time Plotting with Filtering')
mw.resize(800, 800)
cw = QtWidgets.QWidget()
mw.setCentralWidget(cw)
l = QtWidgets.QVBoxLayout()
cw.setLayout(l)


samplingRate = 300


qtPanningPlotRaw = QtPanningPlot(l, "Arduino 1st channel - Raw Data")
qtPanningPlotFiltered = QtPanningPlot(l, "Arduino 1st channel - Filtered Data", filter_enabled=True)

PORT = Arduino.AUTODETECT
board = Arduino(PORT)
digital_pin_5 = board.get_pin('d:5:o') 


initial_max_half = None
threshold_factor = 0.8  
current_max_half = None
samples_buffer = []

def update_threshold(new_data):
    global initial_max_half, current_max_half
    max_half = max(new_data) / 2

    if current_max_half is not None:
        initial_max_half = current_max_half
    else:
        initial_max_half = max_half

    current_max_half = max_half


def check_threshold():
    global initial_max_half, current_max_half
    if current_max_half < initial_max_half * threshold_factor:
        digital_pin_5.write(1)  

def callBack(data):
    global samples_buffer
    samples_buffer.append(data)
    if len(samples_buffer) == 100:
        update_threshold(samples_buffer)
        check_threshold()
        samples_buffer = []
    qtPanningPlotRaw.addData(data)
    qtPanningPlotFiltered.addData(data)




digital_pin_5.write(0)
board.samplingOn(1000 / samplingRate)
board.analog[5].register_callback(callBack)
board.analog[5].enable_reporting()

# Show the window
mw.show()
pg.exec()
board.exit()

print("Finished")