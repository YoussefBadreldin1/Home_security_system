import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtWidgets
from pyfirmata2 import Arduino
from scipy import signal
from iir_filter import IIR_filter 
import time

# filter coefficients
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
            if self.filter_enabled:
                self.plt.setData(x=x, y=self.filtered_data)
            else:
                self.plt.setData(x=x, y=self.data)

    def addData(self, d):
        self.data.append(d)
        if self.filter_enabled:
            filtered_sample = self.iir_filter.filter(d)
            self.filtered_data.append(filtered_sample)

    

# PyQtGraph setup
app = pg.mkQApp()
mw = QtWidgets.QMainWindow()
mw.setWindowTitle('Real-time Plotting with Filtering')
mw.resize(800, 800)
cw = QtWidgets.QWidget()
mw.setCentralWidget(cw)
l = QtWidgets.QVBoxLayout()
cw.setLayout(l)


samplingRate = 300

# Create two plot windows
qtPanningPlotRaw = QtPanningPlot(l, "Arduino 1st channel - Raw Data")
qtPanningPlotFiltered = QtPanningPlot(l, "Arduino 1st channel - Filtered Data", filter_enabled=True)



startTime = 0
sampleCount = 0

def callBack(data):
    global startTime, sampleCount

    sampleCount += 1

    # Calculate sample frequency every 100 samples
    if sampleCount >= 100:
        endTime = time.perf_counter()
        sampleFreq = 100 / (endTime - startTime)  # Calculate frequency directly

        print(f"Sample frequency: {sampleFreq} Hz")

        # Reset for next batch of 100 samples
        sampleCount = 0
        startTime = time.perf_counter()

    
    qtPanningPlotRaw.addData(data)
    qtPanningPlotFiltered.addData(data)

    
# Arduino setup
PORT = Arduino.AUTODETECT
board = Arduino(PORT, debug=True)
board.samplingOn(1000 / samplingRate)
board.analog[5].register_callback(callBack)
board.analog[5].enable_reporting()

# Show the window
mw.show()
pg.exec()
board.exit()

print("Finished")