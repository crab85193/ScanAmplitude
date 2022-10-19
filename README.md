# NI6212 Scan Amplitude
![GitHub watchers](https://img.shields.io/github/watchers/crab85193/ScanAmplitude?style=social)
![Python](https://img.shields.io/badge/python-v3.9.12-007396.svg?logo=python&style=popout)
![PyQt5](https://img.shields.io/badge/PyQt5-v5.15.7-007396.svg?logo=python&style=popout)
![pyqtgraph](https://img.shields.io/badge/pyqtgraph-v0.12.4-007396.svg?logo=python&style=popout)
![pglive](https://img.shields.io/badge/pglive-v0.3.3-007396.svg?logo=python&style=popout)
![nidaqmx](https://img.shields.io/badge/nidaqmx-v0.6.3-44A833.svg?style=popout)

![image](https://github.com/crab85193/ScanAmplitude/blob/main/img/title.PNG)

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

When the application is started, it begins plotting the current analog inputs and outputs.

Press the 'Scan' button to start the operation.

If the operation is started after 'conditioning' is checked, the analog output is increased or decreased until the threshold is reached.
When the threshold is reached, the analog output is fixed and a digital output is made.

If the operation is started without the 'Conditioning' checkbox checked, the analog output will be increased or decreased repeatedly until the 'STOP' button is pressed.
If the threshold is reached during that time, a check will be placed in the checkbox next to the Threshold entry field.

### Digital Output Manual Control

![image](https://github.com/crab85193/ScanAmplitude/blob/main/img/do_manual_control.PNG)

The digital output can be manually controlled in the section of the image above.

### Port Setting

![image](https://github.com/crab85193/ScanAmplitude/blob/main/img/port_setting.PNG)

In the image section above, you can set the analog input/output channels and the digital output ports and lines.
The two digital output ports and lines cannot be set to be the same.

### Parameter Setting

![image](https://github.com/crab85193/ScanAmplitude/blob/main/img/parameter_setting.PNG)

In the part of the image above, you can set the parameters required for the scanning operation.

The threshold value can be set under the 'Threshold Voltage' item.
When the threshold is reached, the checkbox next to it is checked.

The 'Max Voltage' item allows you to set the maximum analog output value.

'Min Voltage' allows you to set the minimum analog output value.

The 'incremental voltage' can be used to set the incremental or decremental value of the analog output per cycle.

Under 'DO when conditioning', you can select the port for the digital output.
When 'DO1' or 'DO2' is selected, one port set in 'Port Setting' is used.
Selecting 'Both' allows the use of two digital output ports.

If something goes wrong, you can restore the initial state by clicking the 'initialize' button at the bottom of the screen.
(Port settings and parameter settings are maintained.)
Pressing the initialize button during scanning operation will stop the operation.

If you want to change the initial values when the application starts, you can do so in 'src/Model.py'.

## Reference
[PyQt5](https://pythonspot.com/pyqt5/)

[PyQtGraph](https://www.pyqtgraph.org/)

[pglive](https://github.com/domarm-comat/pglive)

[NI-DAQmx Python API](https://nidaqmx-python.readthedocs.io/en/latest/)