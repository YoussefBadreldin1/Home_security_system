# Real-Time Data Processing and Door Security System

**Team Number**: 24

**Authors**:
- Mohammed Alqabandi (Student ID: 2675638a)
- Youssef Badreldin (Student ID: 2672792b)

---

## Group Information

**Team Number**: 24

**Members**:
- Mohammed Alqabandi (Student ID: 2675638a)
- Youssef Badreldin (Student ID: 2672792b)

## Project Description

This project consists of two Python scripts that interface with an Arduino for real-time data acquisition and processing in a door security system. The first script performs real-time plotting and filtering of the data, as well as identifying the sampling frequency. The second script enhances door security by using thresholding to determine the state of the door (open/closed).

## Getting Started

### Prerequisites

- Python 3.x
- pyfirmata2 library for Arduino communication
- pyqtgraph for real-time plotting
- scipy for signal processing
- Arduino with standardFirmata firmware

### Installation

To install the required Python libraries, run the following command:

```bash
pip install numpy pyqtgraph pyfirmata2 scipy
```
Additional files:

iir_filter.py file should be located in the same directory as your scripts, or it is installed in your Python environment.

### Usage

Real-Time Plotting/Filtering/Sampling Frequency Identification
Execute the first script to start the real-time data plotting and filtering:

```bash
python real_time_plot_filter.py
```

Door Security System with Thresholding
Launch the second script to activate the door security system:

```bash
python door_security_system.py
```

## Scripts Overview

### real_time_plot_filter.py
Plots and filters real-time data from the Arduino's analog input A5, identifies the sampling frequency.

### door_security_system.py
Plots and filters real-time data from the Arduino's analog input A5, and Monitors a door using thresholding to detect its open/closed status, if the door is opened a signal is sent to digital pin 5 sounding an alarm.


## Hardware Setup


## Contributing
We welcome contributions. Please open an issue to discuss your ideas or submit a pull request.

## Contact
For any queries regarding this project, please contact us:

Mohammed Alqabandi - mohammed_alqabandi@example.com
Youssef Badreldin - youssef_badreldin@example.com


## Acknowledgments
Thank you to all the contributors and instructors who provided guidance for this project.








































