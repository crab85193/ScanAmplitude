from PyQt5.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QLabel,QPushButton,QLineEdit,QComboBox,QCheckBox,QLabel

import pyqtgraph as pg
from pglive.kwargs import Crosshair
from pglive.sources.data_connector import DataConnector
from pglive.sources.live_plot import LiveLinePlot
from pglive.sources.live_plot_widget import LivePlotWidget

import Model
import Controller

class View(QWidget):
    def __init__(self, model: Model):
        super(QWidget, self).__init__()
        self.model = model

    def register(self, controller: Controller):
        self.controller = controller
        self.initUI()
        
    def initUI(self):
        # plot_widget
        kwargs = {Crosshair.ENABLED: True,Crosshair.LINE_PEN: pg.mkPen(color="red", width=1),Crosshair.TEXT_KWARGS: {"color": "green"}}
        plot_ai_widget = LivePlotWidget(title='Analog Input', **kwargs)
        self.plot_ai = LiveLinePlot()
        plot_ai_widget.addItem(self.plot_ai)
        
        plot_ao_widget = LivePlotWidget(title='Analog Output', **kwargs)
        self.plot_ao = LiveLinePlot()
        plot_ao_widget.addItem(self.plot_ao)
        
        plot_group = QVBoxLayout()
        plot_group.addWidget(plot_ai_widget)
        plot_group.addWidget(plot_ao_widget)
        
        # Digital Output manual control area
        do_manual_controllers_group = QVBoxLayout()
        do1_manual_control_area = QHBoxLayout()
        do2_manual_control_area = QHBoxLayout()
        
        do1_label = QLabel('DO1')
        do2_label = QLabel('DO2')
        do1_label.setFixedWidth(160)
        do2_label.setFixedWidth(160)
        
        self.do1_checkbox = QCheckBox()
        self.do2_checkbox = QCheckBox()
        self.do1_checkbox.setFixedWidth(30)
        self.do2_checkbox.setFixedWidth(30)
        
        do1_label.setFixedHeight(15)
        do2_label.setFixedHeight(15)
        
        do1_manual_control_area.addWidget(self.do1_checkbox)
        do1_manual_control_area.addWidget(do1_label)
        do1_manual_control_area.addWidget(QLabel(' '))
        do2_manual_control_area.addWidget(self.do2_checkbox)
        do2_manual_control_area.addWidget(do2_label)
        do2_manual_control_area.addWidget(QLabel(' '))
        
        do_manual_title = QLabel('Digital Output Manual Controller')
        do_manual_title.setFixedHeight(40)
        
        line = QLabel('----------------------------------------')
        line.setFixedHeight(30)
        
        do_manual_controllers_group.addWidget(do_manual_title)
        do_manual_controllers_group.addLayout(do1_manual_control_area)
        do_manual_controllers_group.addLayout(do2_manual_control_area)
        do_manual_controllers_group.addWidget(line)
        
        # Scan Button Area
        scan_button_area = QVBoxLayout()
        conditioning_check_area = QHBoxLayout()
        
        ## Scan Button
        self.scan_button = QPushButton('SCAN')
        self.scan_button.setFixedHeight(80)
        self.scan_button.setCheckable(True)
        self.scan_button.toggled.connect(self.controller.slotScanButtonToggled)
        
        ## Conditioning Checkbox       
        self.conditioning_checkbox = QCheckBox()
        self.conditioning_checkbox.setFixedWidth(30)
        
        conditioning_label = QLabel('Conditioning')
        conditioning_label.setFixedWidth(100)
        conditioning_label.setFixedHeight(40)
        
        conditioning_check_area.addWidget(self.conditioning_checkbox)
        conditioning_check_area.addWidget(conditioning_label)
        conditioning_check_area.addWidget(QLabel(''))
        
        line = QLabel('----------------------------------------')
        line.setFixedHeight(10)
        
        scan_button_area.addWidget(self.scan_button)
        scan_button_area.addLayout(conditioning_check_area)
        scan_button_area.addWidget(line)
        
        # Parameters setting area
        parameters_setting_group = QVBoxLayout()
        threshold_valtage_setting_area = QHBoxLayout()
        max_voltage_setting_area = QHBoxLayout()
        min_voltage_setting_area = QHBoxLayout()
        incremental_voltage_setting_area = QHBoxLayout()
        
        self.threshold = QLineEdit()
        self.vmax = QLineEdit()
        self.vmin = QLineEdit()
        self.vinc = QLineEdit()
        
        self.threshold.setFixedWidth(50)
        self.vmax.setFixedWidth(50)
        self.vmin.setFixedWidth(50)
        self.vinc.setFixedWidth(50)
        
        self.threshold.setText('10.0')
        self.vmax.setText('5.0')
        self.vmin.setText('-5.0')
        self.vinc.setText('0.1')
        
        self.lamp = QCheckBox()
        self.lamp.setEnabled(False)
        
        threshold_label = QLabel('Threshold Voltage')
        vmax_label = QLabel('Max Voltage')
        vmin_label = QLabel('Min Voltage')
        vinc_label = QLabel('Incremental Voltage')
        
        threshold_label.setFixedWidth(110)
        vmax_label.setFixedWidth(110)
        vmin_label.setFixedWidth(110)
        vinc_label.setFixedWidth(110)
        
        threshold_valtage_setting_area.addWidget(threshold_label)
        threshold_valtage_setting_area.addWidget(self.threshold)
        threshold_valtage_setting_area.addWidget(QLabel('V'))
        threshold_valtage_setting_area.addWidget(self.lamp)
        
        max_voltage_setting_area.addWidget(vmax_label)
        max_voltage_setting_area.addWidget(self.vmax)
        max_voltage_setting_area.addWidget(QLabel('V'))
        
        min_voltage_setting_area.addWidget(vmin_label)
        min_voltage_setting_area.addWidget(self.vmin)
        min_voltage_setting_area.addWidget(QLabel('V'))
        
        incremental_voltage_setting_area.addWidget(vinc_label)
        incremental_voltage_setting_area.addWidget(self.vinc)
        incremental_voltage_setting_area.addWidget(QLabel('V'))
                       
        # Digital output port selection area during conditioning
        do_conditioning_area = QHBoxLayout()
        self.do_conditioning_combo = QComboBox()
        items = ['DO1','DO2','Both']
        
        for item in items:
            self.do_conditioning_combo.addItem(item)
            
        self.do_conditioning_combo.setFixedWidth(50) 
        
        do_conditioning_label = QLabel('DO when conditioning')
        do_conditioning_label.setFixedWidth(110)
        
        do_conditioning_area.addWidget(do_conditioning_label)
        do_conditioning_area.addWidget(self.do_conditioning_combo)
        do_conditioning_area.addWidget(QLabel(''))
        
        parameters_setting_group.addLayout(threshold_valtage_setting_area)
        parameters_setting_group.addLayout(max_voltage_setting_area)
        parameters_setting_group.addLayout(min_voltage_setting_area)
        parameters_setting_group.addLayout(incremental_voltage_setting_area)
        parameters_setting_group.addLayout(do_conditioning_area)
        
        # Initialize Button
        self.init_button = QPushButton('Initialize')
        self.init_button.clicked.connect(self.controller.initButtonClecked)
        
        # Set layout
        user_interface = QVBoxLayout()
        user_interface.addLayout(do_manual_controllers_group)
        user_interface.addLayout(scan_button_area)
        user_interface.addLayout(parameters_setting_group)
        user_interface.addWidget(self.init_button)
        
        layout = QHBoxLayout()
        layout.addLayout(plot_group)
        layout.addLayout(user_interface)
        self.setLayout(layout)
        
        self.plot_state = False
        
    def isDO1Checked(self) -> bool:
        return self.do1_checkbox.isChecked()
    
    def isDO2Checked(self) -> bool:
        return self.do2_checkbox.isChecked()
    
    def setDO1Checked(self, checked: bool) -> None:
        self.do1_checkbox.setChecked(checked)
        
    def setDO2Checked(self, checked: bool) -> None:
        self.do2_checkbox.setChecked(checked)
        
    def setScanBottonText(self, text: str) -> None:
        self.scan_button.setText(text)
        
    def isConditioningChecked(self) -> bool:
        return self.conditioning_checkbox.isChecked()
    
    def setConditioningChecked(self, checked: bool) -> None:
        self.conditioning_checkbox.setChecked(checked)
    
    def getThresholdText(self) -> str:
        return self.threshold.text()
    
    def getThresholdValue(self) -> float:
        return float(self.threshold.text())
    
    def getVmaxText(self) -> str:
        return self.vmax.text()
    
    def getVmaxValue(self) -> float:
        return float(self.vmax.text())
    
    def getVminText(self) -> str:
        return self.vmin.text()
    
    def getVminValue(self) -> float:
        return float(self.vmin.text())
    
    def getVincText(self) -> str:
        return self.vinc.text()
    
    def getVincValue(self) -> float:
        return float(self.vinc.text())
    
    def getLampState(self) -> bool:
        return self.lamp.isChecked()
    
    def setLampState(self, state: bool) -> None:
        return self.lamp.setChecked(state)
    
    def getDOConditioningCurrentText(self) -> str:
        return self.do_conditioning_combo.currentText()
    
    def getDOConditioningCurrentIndex(self) -> int:
        return self.do_conditioning_combo.currentIndex()
    
    def getPlotState(self) -> bool:
        return self.plot_state
    
    def setPlotState(self, state: bool) -> None:
        self.plot_state = state
        
    def getPlotAI(self) -> LiveLinePlot:
        return self.plot_ai
    
    def getPlotAO(self) -> LiveLinePlot:
        return self.plot_ao