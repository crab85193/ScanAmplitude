from pglive.sources.data_connector import DataConnector
import time

from NIDAQmxController import NIDAQ_ai_task,NIDAQ_ao_task,NIDAQ_do_task

from ScanAmplitude import ScanAmplitude
from DOManualController import DOManualController

import Model
import View

class Controller(object):
    def __init__(self, model: Model, view: View):
        self.model = model
        self.view = view
        self.view.register(self)
        
        ai_task = NIDAQ_ai_task('ai0')
        ao_task = NIDAQ_ao_task('ao0')
        do_tasks = [NIDAQ_do_task('port1','line0'),NIDAQ_do_task('port1','line1')]
        
        self.scan_amplitude = ScanAmplitude(ai_task,ao_task,do_tasks)
        self.do_manual_controller = DOManualController(do_tasks)
        
        self.scan_amplitude.taskStart()
        
    def slotScanButtonToggled(self, checked: bool) -> None:
        if checked:
            # self.scan_amplitude.initialize()
            self.plot_state = True
            if self.view.getDOConditioningCurrentText() == 'Both':
                do_port_state = [True,True]
            elif self.view.getDOConditioningCurrentText() == 'DO1':
                do_port_state = [True,False]
            elif self.view.getDOConditioningCurrentText() == 'DO2':
                do_port_state = [False,True]
            else:
                do_port_state = [False,False]
                
            self.scan_amplitude.setConditioningState(self.view.isConditioningChecked())
            self.scan_amplitude.setParameters(self.plot_state,self.view.getThresholdValue(),self.view.getVmaxValue(),self.view.getVminValue(),self.view.getVincValue(),do_port_state)
            
            self.view.setDO1Checked(False)
            self.view.setDO2Checked(False)
            self.view.setLampState(False)
            self.view.setScanBottonText('STOP')
        else:
            self.plot_state = False
            self.scan_amplitude.setParameters(self.plot_state,0.0,0.0,0.0,0.0,[False,False])
            self.view.setScanBottonText('SCAN')
            
    def initButtonClecked(self) -> None:
        self.view.setDO1Checked(False)
        self.view.setDO2Checked(False)
        self.view.setConditioningChecked(False)
        self.view.setLampState(False)
        
        self.scan_amplitude.initialize()
        
    def doController(self) -> None:
        while True:
            self.do_manual_controller.setDOState(0,self.view.isDO1Checked())
            self.do_manual_controller.setDOState(1,self.view.isDO2Checked())
            self.view.setLampState(self.scan_amplitude.getThresholdState())
            
            if self.scan_amplitude.getThresholdState():
                self.view.setDO1Checked(self.do_manual_controller.getDOState(0))
                self.view.setDO2Checked(self.do_manual_controller.getDOState(1))
            
    def aiPlotGenerator(self, *data_connectors: tuple) -> None:
        x = 0
        while True:
            for data_connector in data_connectors:
                data_connector.cb_append_data_point(self.scan_amplitude.getAIMessageBox(),x)
                x += 1

            time.sleep(0.025)
            
    def aoPlotGenerator(self, *data_connectors: tuple) -> None:
        x = 0
        while True:
            for data_connector in data_connectors:
                data_connector.cb_append_data_point(self.scan_amplitude.getAOMessageBox(),x)
                x += 1

            time.sleep(0.025)
    
            