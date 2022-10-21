from PyQt5.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QLabel,QPushButton,QLineEdit,QComboBox,QCheckBox,QLabel
import pyqtgraph as pg
from pglive.kwargs import Crosshair
from pglive.sources.live_plot import LiveLinePlot
from pglive.sources.live_plot_widget import LivePlotWidget
import Model
import Controller

class View(QWidget):
    def __init__(self, model: Model):
        super(QWidget, self).__init__()
        self.__model = model
        self.__plot_state = False

    def register(self, controller: Controller) -> None:
        self.__controller = controller
        self.__initUI()
        
    def __initUI(self) -> None:
        # Plot Widget
        kwargs = {Crosshair.ENABLED: True,Crosshair.LINE_PEN: pg.mkPen(color="red", width=1),Crosshair.TEXT_KWARGS: {"color": "green"}}
        self.__plot_ai = LiveLinePlot()
        self.__plot_ao = LiveLinePlot() 
        ## Analog Input Plot Widget
        plot_ai_widget = LivePlotWidget(title=self.__model.getAIPlotTitle(), **kwargs)
        plot_ai_widget.addItem(self.__plot_ai)
        ## Analog Output Plot Widget
        plot_ao_widget = LivePlotWidget(title=self.__model.getAOPlotTitle(), **kwargs)
        plot_ao_widget.addItem(self.__plot_ao)
        ## Plot Grouping
        plot_group = QVBoxLayout()
        ### Add Widget
        plot_group.addWidget(plot_ai_widget)
        plot_group.addWidget(plot_ao_widget)
        
        # Digital Output manual control area
        ## Title
        do_manual_title = QLabel(self.__model.getDOManualTitle())
        do_manual_title.setFixedHeight(40)
        ## CheckboxLabel
        do1_checkbox_label = QLabel(self.__model.getDO1CheckboxLabel())
        do2_checkbox_label = QLabel(self.__model.getDO2CheckboxLabel())
        do1_checkbox_label.setFixedWidth(160)
        do2_checkbox_label.setFixedWidth(160)
        do1_checkbox_label.setFixedHeight(15)
        do2_checkbox_label.setFixedHeight(15)
        ## Line
        line = QLabel(self.__model.getLine())
        line.setFixedHeight(10)
        ## Checkbox
        self.__do1_checkbox = QCheckBox()
        self.__do2_checkbox = QCheckBox()
        self.__do1_checkbox.setFixedWidth(30)
        self.__do2_checkbox.setFixedWidth(30)
        ## Digital Output Manual Controllers Grouping
        do_manual_controllers_group = QVBoxLayout()
        do1_manual_control_area = QHBoxLayout()
        do2_manual_control_area = QHBoxLayout()
        ### Add Widget
        do1_manual_control_area.addWidget(self.__do1_checkbox)
        do1_manual_control_area.addWidget(do1_checkbox_label)
        do1_manual_control_area.addWidget(QLabel(' '))
        do2_manual_control_area.addWidget(self.__do2_checkbox)
        do2_manual_control_area.addWidget(do2_checkbox_label)
        do2_manual_control_area.addWidget(QLabel(' '))
        do_manual_controllers_group.addWidget(do_manual_title)
        do_manual_controllers_group.addLayout(do1_manual_control_area)
        do_manual_controllers_group.addLayout(do2_manual_control_area)
        do_manual_controllers_group.addWidget(line)
        
        # Scan Button Area
        ## Label
        conditioning_label = QLabel(self.__model.getConditioningLabel())
        line = QLabel(self.__model.getLine())
        ### Set Fixed Width
        conditioning_label.setFixedWidth(100)
        ### Set Fixed Height
        conditioning_label.setFixedHeight(40)
        line.setFixedHeight(10)
        ## Scan Button
        self.__scan_button = QPushButton(self.__model.getScanButtonLabel(False))
        self.__scan_button.setFixedHeight(40)
        self.__scan_button.setCheckable(True)
        self.__scan_button.toggled.connect(self.__controller.slotScanButtonToggled)
        ## Conditioning Checkbox
        self.__conditioning_checkbox = QCheckBox()
        self.__conditioning_checkbox.setFixedWidth(30)
        ## Scan Button Area Grouping
        scan_button_area = QVBoxLayout()
        conditioning_check_area = QHBoxLayout()
        ### Add Widget
        conditioning_check_area.addWidget(self.__conditioning_checkbox)
        conditioning_check_area.addWidget(conditioning_label)
        conditioning_check_area.addWidget(QLabel(''))
        ### Grouping
        scan_button_area.addWidget(self.__scan_button)
        scan_button_area.addLayout(conditioning_check_area)
        scan_button_area.addWidget(line)
        
        # Port Setting Area
        ## Label
        ai_channel_label = QLabel(self.__model.getAIChannelLabel())
        ao_channel_label = QLabel(self.__model.getAOChannelLabel())
        do1_port_and_line_label = QLabel(self.__model.getDO1PortAndLineLabel())
        do2_port_and_line_label = QLabel(self.__model.getDO2PortAndLineLabel())
        line = QLabel(self.__model.getLine())
        ### Set Fixed Height
        line.setFixedHeight(10)
        ## Port Select Combo
        self.__ai_channel_combo = QComboBox()
        self.__ao_channel_combo = QComboBox()
        self.__do1_port_combo = QComboBox()
        self.__do1_line_combo = QComboBox()
        self.__do2_port_combo = QComboBox()
        self.__do2_line_combo = QComboBox()
        ### Add Items
        self.__ai_channel_combo.addItems(self.__model.getAIChannels())
        self.__ao_channel_combo.addItems(self.__model.getAOChannels())
        self.__do1_port_combo.addItems(self.__model.getDOPorts())
        self.__do1_line_combo.addItems(self.__model.getDOLines())
        self.__do2_port_combo.addItems(self.__model.getDOPorts())
        self.__do2_line_combo.addItems(self.__model.getDOLines())
        ### Set Default Index
        self.__ai_channel_combo.setCurrentIndex(self.__model.getAIChannelsDefaultIndex())
        self.__ao_channel_combo.setCurrentIndex(self.__model.getAOChannelsDefaultIndex())
        self.__do1_port_combo.setCurrentIndex(self.__model.getDO1PortsDefaultIndex())
        self.__do1_line_combo.setCurrentIndex(self.__model.getDO1LinesDefaultIndex())
        self.__do2_port_combo.setCurrentIndex(self.__model.getDO2PortsDefaultIndex())
        self.__do2_line_combo.setCurrentIndex(self.__model.getDO2LinesDefaultIndex())
        ## Port Setting Area Grouping
        port_setting_group = QVBoxLayout()
        ai_setting_area = QHBoxLayout()
        ao_setting_area = QHBoxLayout()
        do1_setting_area = QHBoxLayout()
        do2_setting_area = QHBoxLayout()
        ### AddWidget
        ai_setting_area.addWidget(ai_channel_label)
        ai_setting_area.addWidget(self.__ai_channel_combo)
        ao_setting_area.addWidget(ao_channel_label)
        ao_setting_area.addWidget(self.__ao_channel_combo)
        do1_setting_area.addWidget(do1_port_and_line_label)
        do1_setting_area.addWidget(self.__do1_port_combo)
        do1_setting_area.addWidget(self.__do1_line_combo)
        do2_setting_area.addWidget(do2_port_and_line_label)
        do2_setting_area.addWidget(self.__do2_port_combo)
        do2_setting_area.addWidget(self.__do2_line_combo)
        ### Grouping
        port_setting_group.addLayout(ai_setting_area)
        port_setting_group.addLayout(ao_setting_area)
        port_setting_group.addLayout(do1_setting_area)
        port_setting_group.addLayout(do2_setting_area)
        port_setting_group.addWidget(line)
        
        # Parameters Setting Area
        ## Label
        threshold_label = QLabel(self.__model.getThresholdLabel())
        vmax_label = QLabel(self.__model.getVmaxLabel())
        vmin_label = QLabel(self.__model.getVminLabel())
        vinc_label = QLabel(self.__model.getVincLabel())
        do_conditioning_label = QLabel(self.__model.getDOConditioningLabel())
        ### Set Fixed Width
        threshold_label.setFixedWidth(110)
        vmax_label.setFixedWidth(110)
        vmin_label.setFixedWidth(110)
        vinc_label.setFixedWidth(110)
        do_conditioning_label.setFixedWidth(110)
        ## Text Box
        self.__threshold = QLineEdit()
        self.__vmax = QLineEdit()
        self.__vmin = QLineEdit()
        self.__vinc = QLineEdit()
        ### Set Fixed Width
        self.__threshold.setFixedWidth(50)
        self.__vmax.setFixedWidth(50)
        self.__vmin.setFixedWidth(50)
        self.__vinc.setFixedWidth(50)
        ### Set Default Text
        self.__threshold.setText(self.__model.getThresholdDefaultValue())
        self.__vmax.setText(self.__model.getVmaxDefaultValue())
        self.__vmin.setText(self.__model.getVminDefaultValue())
        self.__vinc.setText(self.__model.getVincDefaultValue())
        ## Lamp
        self.__lamp = QCheckBox()
        self.__lamp.setEnabled(False)
        ## Digital Output Port Combo
        self.__do_conditioning_combo = QComboBox()
        self.__do_conditioning_combo.setFixedWidth(50) 
        self.__do_conditioning_combo.addItems(self.__model.getDOConditioningItems())
        ## Parameters Setting Area Grouping
        parameters_setting_group = QVBoxLayout()
        threshold_valtage_setting_area = QHBoxLayout()
        max_voltage_setting_area = QHBoxLayout()
        min_voltage_setting_area = QHBoxLayout()
        incremental_voltage_setting_area = QHBoxLayout()
        ### Add Widget
        threshold_valtage_setting_area.addWidget(threshold_label)
        threshold_valtage_setting_area.addWidget(self.__threshold)
        threshold_valtage_setting_area.addWidget(QLabel('V'))
        threshold_valtage_setting_area.addWidget(self.__lamp)
        max_voltage_setting_area.addWidget(vmax_label)
        max_voltage_setting_area.addWidget(self.__vmax)
        max_voltage_setting_area.addWidget(QLabel('V'))
        min_voltage_setting_area.addWidget(vmin_label)
        min_voltage_setting_area.addWidget(self.__vmin)
        min_voltage_setting_area.addWidget(QLabel('V'))
        incremental_voltage_setting_area.addWidget(vinc_label)
        incremental_voltage_setting_area.addWidget(self.__vinc)
        incremental_voltage_setting_area.addWidget(QLabel('V'))     
        ### Digital Output Port Selection Area 
        do_conditioning_area = QHBoxLayout()
        do_conditioning_area.addWidget(do_conditioning_label)
        do_conditioning_area.addWidget(self.__do_conditioning_combo)
        do_conditioning_area.addWidget(QLabel(''))
        ### Grouping
        parameters_setting_group.addLayout(threshold_valtage_setting_area)
        parameters_setting_group.addLayout(max_voltage_setting_area)
        parameters_setting_group.addLayout(min_voltage_setting_area)
        parameters_setting_group.addLayout(incremental_voltage_setting_area)
        parameters_setting_group.addLayout(do_conditioning_area)
        
        # Initialize Button
        self.__init_button = QPushButton(self.__model.getInitButtonLabel())
        self.__init_button.clicked.connect(self.__controller.initButtonClecked)
        
        # Set layout
        user_interface = QVBoxLayout()
        layout = QHBoxLayout()
        user_interface.addLayout(do_manual_controllers_group)
        user_interface.addLayout(scan_button_area)
        user_interface.addLayout(port_setting_group)
        user_interface.addLayout(parameters_setting_group)
        user_interface.addWidget(self.__init_button)
        layout.addLayout(plot_group)
        layout.addLayout(user_interface)
        self.setLayout(layout)
    
    def initDO1PortCombo(self) -> None:
        self.__do1_port_combo.clear()
        self.__do1_port_combo.addItems(self.__model.getDOPorts())
    
    def initDO1LineCombo(self) -> None:
        self.__do1_line_combo.clear()
        self.__do1_line_combo.addItems(self.__model.getDOLines())
        
    def initDO2PortCombo(self) -> None:
        self.__do2_port_combo.clear()
        self.__do2_port_combo.addItems(self.__model.getDOPorts())
    
    def initDO2LineCombo(self) -> None:
        self.__do2_line_combo.clear()
        self.__do2_line_combo.addItems(self.__model.getDOLines())
    
    def isDO1Checked(self) -> bool:
        return self.__do1_checkbox.isChecked()
    
    def isDO2Checked(self) -> bool:
        return self.__do2_checkbox.isChecked()
    
    def isConditioningChecked(self) -> bool:
        return self.__conditioning_checkbox.isChecked()
    
    def getAIChannel(self) -> str:
        return self.__ai_channel_combo.currentText()
    
    def getAIChannelComboCurrentIndex(self) -> int:
        return self.__ai_channel_combo.currentIndex()
    
    def getAOChannel(self) -> str:
        return self.__ao_channel_combo.currentText()
    
    def getAOChannelComboCurrentIndex(self) -> int:
        return self.__ao_channel_combo.currentIndex()
    
    def getDO1Port(self) -> str:
        return self.__do1_port_combo.currentText()
    
    def getDO1PortComboIndex(self) -> int:
        return self.__do1_port_combo.currentIndex()
    
    def getDO1PortComboFindText(self, text: str) -> int:
        return self.__do1_port_combo.findText(text)
    
    def getDO1Line(self) -> str:
        return self.__do1_line_combo.currentText()
    
    def getDO1LineComboIndex(self) -> int:
        return self.__do1_line_combo.currentIndex()
    
    def getDO1LineComboFindText(self, text: str) -> int:
        return self.__do1_line_combo.findText(text)
    
    def getDO2Port(self) -> str:
        return self.__do2_port_combo.currentText()
    
    def getDO2PortComboIndex(self) -> int:
        return self.__do2_port_combo.currentIndex()
    
    def getDO2PortComboFindText(self, text: str) -> int:
        return self.__do2_port_combo.findText(text)
    
    def getDO2Line(self) -> str:
        return self.__do2_line_combo.currentText()
    
    def getDO2LineComboIndex(self) -> int:
        return self.__do2_line_combo.currentIndex()
    
    def getDO2LineComboFindText(self, text: str) -> int:
        return self.__do2_line_combo.findText(text)
    
    def getThresholdText(self) -> str:
        return self.__threshold.text()
    
    def getThresholdValue(self) -> float:
        return float(self.__threshold.text())
    
    def getVmaxText(self) -> str:
        return self.__vmax.text()
    
    def getVmaxValue(self) -> float:
        return float(self.__vmax.text())
    
    def getVminText(self) -> str:
        return self.__vmin.text()
    
    def getVminValue(self) -> float:
        return float(self.__vmin.text())
    
    def getVincText(self) -> str:
        return self.__vinc.text()
    
    def getVincValue(self) -> float:
        return float(self.__vinc.text())
    
    def getLampState(self) -> bool:
        return self.__lamp.isChecked()
    
    def getDOConditioningCurrentText(self) -> str:
        return self.__do_conditioning_combo.currentText()
    
    def getDOConditioningCurrentIndex(self) -> int:
        return self.__do_conditioning_combo.currentIndex()
    
    def getPlotState(self) -> bool:
        return self.__plot_state
    
    def getPlotAI(self) -> LiveLinePlot:
        return self.__plot_ai
    
    def getPlotAO(self) -> LiveLinePlot:
        return self.__plot_ao
    
    def setDO1Checked(self, checked: bool) -> None:
        self.__do1_checkbox.setChecked(checked)
        
    def setDO2Checked(self, checked: bool) -> None:
        self.__do2_checkbox.setChecked(checked)
        
    def setScanBottonText(self, text: str) -> None:
        self.__scan_button.setText(text)
    
    def setScanButtonState(self, state: bool) -> None:
        self.__scan_button.setChecked(state)
    
    def setConditioningEnabled(self, state: bool) -> None:
        self.__conditioning_checkbox.setEnabled(state)
    
    def setConditioningChecked(self, checked: bool) -> None:
        self.__conditioning_checkbox.setChecked(checked)

    def setAIChannelComboEnabled(self, state: bool) -> None:
        self.__ai_channel_combo.setEnabled(state)
        
    def setAOChannelComboEnabled(self, state: bool) -> None:
        self.__ao_channel_combo.setEnabled(state)
    
    def setDO1PortComboEnabled(self, state: bool) -> None:
        self.__do1_port_combo.setEnabled(state)
    
    def setDO1PortComboCurrentIndex(self, index: int) -> None:
        self.__do1_port_combo.setCurrentIndex(index)
    
    def setDO1LineComboEnabled(self, state: bool) -> None:
        self.__do1_line_combo.setEnabled(state)
    
    def setDO1LineComboCurrentIndex(self, index: int) -> None:
        self.__do1_line_combo.setCurrentIndex(index)
    
    def setDO2PortComboEnabled(self, state: bool) -> None:
        self.__do2_port_combo.setEnabled(state)
    
    def setDO2PortComboCurrentIndex(self, index: int) -> None:
        self.__do2_port_combo.setCurrentIndex(index)
    
    def setDO2LineComboEnabled(self, state: bool) -> None:
        self.__do2_line_combo.setEnabled(state)
    
    def setDO2LineComboCurrentIndex(self, index: int) -> None:
        self.__do2_line_combo.setCurrentIndex(index)
    
    def setLampState(self, state: bool) -> None:
        self.__lamp.setChecked(state)
    
    def setThresholdTextBoxEnabled(self, state: bool) -> None:
        self.__threshold.setEnabled(state)
        
    def setVmaxTextBoxEnabled(self, state: bool) -> None:
        self.__vmax.setEnabled(state)
    
    def setVminTextBoxEnabled(self, state: bool) -> None:
        self.__vmin.setEnabled(state)
        
    def setVincTextBoxEnabled(self, state: bool) -> None:
        self.__vinc.setEnabled(state)
        
    def setDOConditioningComboEnabled(self, state: bool) -> None:
        self.__do_conditioning_combo.setEnabled(state)
    
    def setPlotState(self, state: bool) -> None:
        self.__plot_state = state
    
    def removeDO1PortComboItem(self, index: int) -> None:
        self.__do1_port_combo.removeItem(index)
    
    def removeDO1LineComboItem(self, index: int) -> None:
        self.__do1_line_combo.removeItem(index)
        
    def removeDO2PortComboItem(self, index: int) -> None:
        self.__do2_port_combo.removeItem(index)
        
    def removeDO2LineComboItem(self, index: int) -> None:
        self.__do2_line_combo.removeItem(index)