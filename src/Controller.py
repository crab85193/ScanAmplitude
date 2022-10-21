import time
import Model
import View
from NIDAQmxController import NIDAQ_ai_task,NIDAQ_ao_task,NIDAQ_do_task
from ScanAmplitude import ScanAmplitude
from DOManualController import DOManualController

class Controller(object):
    def __init__(self, model: Model, view: View):
        self.__model = model
        self.__view = view
        self.__view.register(self)
        
        self.__ai_task = NIDAQ_ai_task()
        self.__ao_task = NIDAQ_ao_task()
        self.__do_tasks = [NIDAQ_do_task(),NIDAQ_do_task()]
        
        self.__scan_amplitude = ScanAmplitude(self.__ai_task,self.__ao_task)
        self.__do_manual_controller = DOManualController(self.__do_tasks)
        
        self.__ai_plot_counter = 0
        self.__ao_plot_counter = 0
        
        self.__seveUserSelectInformation()
        self.__initTask()
            
    def __seveUserSelectInformation(self) -> None:
        self.__ai_old_channel_index = self.__view.getAIChannelComboCurrentIndex()
        self.__ao_old_channel_index = self.__view.getAOChannelComboCurrentIndex()
        self.__do1_old_port_index = self.__view.getDO1PortComboIndex()
        self.__do1_old_line_index = self.__view.getDO1LineComboIndex()
        self.__do2_old_port_index = self.__view.getDO2PortComboIndex()
        self.__do2_old_line_index = self.__view.getDO2LineComboIndex()
    
    def __updateDOPortComboAndLineCombo(self) -> None:
        do1_port = self.__view.getDO1Port()
        do1_line = self.__view.getDO1Line()
        do2_port = self.__view.getDO2Port()
        do2_line = self.__view.getDO2Line()
        
        self.__view.initDO1LineCombo()
        self.__view.initDO2LineCombo()
        
        do1_line_combo_current_index = self.__view.getDO1LineComboFindText(do1_line)
        do2_line_combo_current_index = self.__view.getDO2LineComboFindText(do2_line)
        
        if do1_port == do2_port:
            if do1_line_combo_current_index == do2_line_combo_current_index:
                if do2_line_combo_current_index < 7:
                    do2_line_combo_current_index += 1
                else:
                    do2_line_combo_current_index -= 1
            
            self.__view.setDO1LineComboCurrentIndex(do1_line_combo_current_index)
            self.__view.setDO2LineComboCurrentIndex(do2_line_combo_current_index)
            
            do1_line_combo_remove_index = do2_line_combo_current_index
            do2_line_combo_remove_index = do1_line_combo_current_index
            
            self.__view.removeDO1LineComboItem(do1_line_combo_remove_index)
            self.__view.removeDO2LineComboItem(do2_line_combo_remove_index)
        else:
            self.__view.setDO1LineComboCurrentIndex(do1_line_combo_current_index)
            self.__view.setDO2LineComboCurrentIndex(do2_line_combo_current_index)
        
        self.__seveUserSelectInformation()
    
    def __initTask(self) -> None:
        self.__ai_task.createTask(self.__view.getAIChannel())
        self.__ai_task.start()
        self.__ao_task.createTask(self.__view.getAOChannel())
        self.__ao_task.start()
        self.__do_tasks[0].createTask(self.__view.getDO1Port(),self.__view.getDO1Line())
        self.__do_tasks[0].start()
        self.__do_tasks[1].createTask(self.__view.getDO2Port(),self.__view.getDO2Line())
        self.__do_tasks[1].start()
        self.__view.removeDO1LineComboItem(self.__do2_old_line_index)
        self.__view.removeDO2LineComboItem(self.__do1_old_line_index)
        
        self.__seveUserSelectInformation()
            
    def __updateTask(self) -> None:
        ai_channel_changed = self.__ai_old_channel_index != self.__view.getAIChannelComboCurrentIndex()
        ao_channel_changed = self.__ao_old_channel_index != self.__view.getAOChannelComboCurrentIndex()
        do1_port_changed = self.__do1_old_port_index != self.__view.getDO1PortComboIndex()
        do1_line_changed = self.__do1_old_line_index != self.__view.getDO1LineComboIndex()
        do2_port_changed = self.__do2_old_port_index != self.__view.getDO2PortComboIndex()
        do2_line_changed = self.__do2_old_line_index != self.__view.getDO2LineComboIndex()
        
        if ai_channel_changed:
            self.__ai_task.createTask(self.__view.getAIChannel())
            self.__ai_task.start()
        if ao_channel_changed:
            self.__ao_task.createTask(self.__view.getAOChannel())
            self.__ao_task.start()
        if (do1_port_changed or do1_line_changed) or (do2_port_changed or do2_line_changed):
            self.__updateDOPortComboAndLineCombo()
            self.__do_tasks[0].createTask(self.__view.getDO1Port(),self.__view.getDO1Line())
            self.__do_tasks[1].createTask(self.__view.getDO2Port(),self.__view.getDO2Line())
            self.__do_tasks[0].start()
            self.__do_tasks[1].start()
        
        self.__seveUserSelectInformation()
    
    def __setConditioningCheckBoxEnabled(self, state: bool) -> None:
        self.__view.setConditioningEnabled(state)
    
    def __setPortSettingComboEnabled(self, state: bool) -> None:
        self.__view.setAIChannelComboEnabled(state)
        self.__view.setAOChannelComboEnabled(state)
        self.__view.setDO1PortComboEnabled(state)
        self.__view.setDO1LineComboEnabled(state)
        self.__view.setDO2PortComboEnabled(state)
        self.__view.setDO2LineComboEnabled(state)
    
    def __setParameterSettingTextBoxEnabled(self, state: bool) -> None:
        self.__view.setThresholdTextBoxEnabled(state)
        self.__view.setVmaxTextBoxEnabled(state)
        self.__view.setVminTextBoxEnabled(state)
        self.__view.setVincTextBoxEnabled(state)
        self.__view.setDOConditioningComboEnabled(state)
    
    def slotScanButtonToggled(self, checked: bool) -> None:
        if checked:            
            self.__scan_amplitude.initFlag()
            self.__plot_state = True
            if self.__view.getDOConditioningCurrentText() == 'Both':
                do_port_state = [True,True]
            elif self.__view.getDOConditioningCurrentText() == 'DO1':
                do_port_state = [True,False]
            elif self.__view.getDOConditioningCurrentText() == 'DO2':
                do_port_state = [False,True]
            else:
                do_port_state = [False,False]
                
            self.__scan_amplitude.setConditioningState(self.__view.isConditioningChecked())
            self.__scan_amplitude.setParameters(self.__plot_state,self.__view.getThresholdValue(),self.__view.getVmaxValue(),self.__view.getVminValue(),self.__view.getVincValue(),do_port_state)
            
            self.__view.setDO1Checked(False)
            self.__view.setDO2Checked(False)
            self.__view.setLampState(False)
            
            self.__setConditioningCheckBoxEnabled(False)
            self.__setPortSettingComboEnabled(False)
            self.__setParameterSettingTextBoxEnabled(False)
            
            self.__view.setScanBottonText(self.__model.getScanButtonLabel(True))
        else:
            self.__plot_state = False
            self.__scan_amplitude.setParameters(self.__plot_state,0.0,0.0,0.0,0.0,[False,False])
            
            self.__setConditioningCheckBoxEnabled(True)
            self.__setPortSettingComboEnabled(True)
            self.__setParameterSettingTextBoxEnabled(True)
            
            self.__view.setScanBottonText(self.__model.getScanButtonLabel(False))
            
    def initButtonClecked(self) -> None:
        self.__view.setDO1Checked(False)
        self.__view.setDO2Checked(False)
        self.__view.setLampState(False)
        self.__view.setScanButtonState(False)
        
        self.__setConditioningCheckBoxEnabled(True)
        self.__setPortSettingComboEnabled(True)
        self.__setParameterSettingTextBoxEnabled(True)
        
        self.__view.initDO1LineCombo()
        self.__view.initDO2LineCombo()
        self.__view.setDO2LineComboCurrentIndex(1)
        
        self.__scan_amplitude.initialize()

    def aiPlotGenerator(self, *data_connectors: tuple) -> None:
        for data_connector in data_connectors:
            data_connector.cb_append_data_point(self.__scan_amplitude.getAIMessageBox(),self.__ai_plot_counter)
            self.__ai_plot_counter += 1
        time.sleep(0.1)
        
    def aoPlotGenerator(self, *data_connectors: tuple) -> None:
        for data_connector in data_connectors:
            data_connector.cb_append_data_point(self.__scan_amplitude.getAOMessageBox(),self.__ao_plot_counter)
            self.__ao_plot_counter += 1
        time.sleep(0.1)
    
    def doController(self) -> None:
        self.__do_manual_controller.setDOState(0,self.__view.isDO1Checked())
        self.__do_manual_controller.setDOState(1,self.__view.isDO2Checked())
        self.__view.setLampState(self.__scan_amplitude.getThresholdState())
        
        if self.__scan_amplitude.getThresholdState():
            self.__view.setDO1Checked(self.__scan_amplitude.getDOState(0))
            self.__view.setDO2Checked(self.__scan_amplitude.getDOState(1))
    
    def executeScan(self) -> None:
        self.__updateTask()
        self.__scan_amplitude.scan()
        self.doController()