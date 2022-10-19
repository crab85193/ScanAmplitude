# NI6212 Scan Amplitude
![GitHub watchers](https://img.shields.io/github/watchers/crab85193/ScanAmplitude_mvc?style=social)
![Python](https://img.shields.io/badge/python-v3.9.12-007396.svg?logo=python&style=popout)
![PyQt5](https://img.shields.io/badge/PyQt5-v5.15.7-007396.svg?logo=python&style=popout)
![pyqtgraph](https://img.shields.io/badge/pyqtgraph-v0.12.4-007396.svg?logo=python&style=popout)
![pglive](https://img.shields.io/badge/pglive-v0.3.3-007396.svg?logo=python&style=popout)
![nidaqmx](https://img.shields.io/badge/nidaqmx-v0.6.3-44A833.svg?style=popout)

![image](https://github.com/crab85193/ScanAmplitude_mvc/blob/develop/img/title.PNG)

This is a GUI application developed for NATIONAL INSTRUMENTS' NI USB-6212 BNC BUS-POWERED M SE.

## Requirement
- Windows10
- Python 3.9.12
- PyQt5 5.15.7
- pyqtgraph 0.12.4
- pglive 0.3.3
- nidaqmx 0.6.3

## Usage
To run this application, run src/App.py.

```
$ cd src

$ python App.py
```

or

```
$ python src/App.py
```

## Description
This application allows you to perform scanning operations.

The analog output is gradually increased until the analog input reaches the threshold value.
When the analog input reaches the threshold value, the analog output stops increasing or decreasing and a digital signal is output.

![image](https://github.com/crab85193/ScanAmplitude_mvc/blob/develop/img/do_manual_control.PNG)
![image](https://github.com/crab85193/ScanAmplitude_mvc/blob/develop/img/parameter_setting.PNG)
![image](https://github.com/crab85193/ScanAmplitude_mvc/blob/develop/img/port_setting.PNG)

## Reference
[PyQt5](https://pythonspot.com/pyqt5/)

[PyQtGraph](https://www.pyqtgraph.org/)

[pglive](https://github.com/domarm-comat/pglive)

[NI-DAQmx Python API](https://nidaqmx-python.readthedocs.io/en/latest/)