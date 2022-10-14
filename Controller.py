from pglive.sources.data_connector import DataConnector
import time

from threading import Thread

from NIDAQmxController import NIDAQ_ai_task,NIDAQ_ao_task,NIDAQ_do_task

from ScanAmplitude import ScanAmplitude
from DOManualController import DOManualController

import Model
import View

class Controller(object):
    def __init__(self, model: Model, view: View):
        self.__model = model
        self.__view = view
        self.__view.register(self)
        
        self.__ai_plot_counter = 0
        self.__ao_plot_counter = 0
        
        self.__ai_old_channel = None
        self.__ao_old_channel = None
        self.__do1_old_port = None
        self.__do1_old_line = None
        self.__do2_old_port = None
        self.__do2_old_line = None
        
        self.__ai_task = NIDAQ_ai_task()
        self.__ao_task = NIDAQ_ao_task()
        self.__do_tasks = [NIDAQ_do_task(),NIDAQ_do_task()]
        
        self.__updateTask()
        
        self.__scan_amplitude = ScanAmplitude(self.__ai_task,self.__ao_task,self.__do_tasks)
        self.__do_manual_controller = DOManualController(self.__do_tasks)
        
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
            self.__view.setScanBottonText(self.__model.getScanButtonLabel(True))
        else:
            self.__plot_state = False
            self.__scan_amplitude.setParameters(self.__plot_state,0.0,0.0,0.0,0.0,[False,False])
            self.__view.setScanBottonText(self.__model.getScanButtonLabel(False))
            
    def initButtonClecked(self) -> None:
        self.__view.setDO1Checked(False)
        self.__view.setDO2Checked(False)
        self.__view.setConditioningChecked(False)
        self.__view.setLampState(False)
        self.__view.setScanButtonState(False)
        
        self.__scan_amplitude.initialize()
        
    def doController(self) -> None:
        self.__do_manual_controller.setDOState(0,self.__view.isDO1Checked())
        self.__do_manual_controller.setDOState(1,self.__view.isDO2Checked())
        self.__view.setLampState(self.__scan_amplitude.getThresholdState())
        
        if self.__scan_amplitude.getThresholdState():
            self.__view.setDO1Checked(self.__scan_amplitude.getDOState(0))
            self.__view.setDO2Checked(self.__scan_amplitude.getDOState(1))

    def aiPlotGenerator(self, *data_connectors: tuple) -> None:
        for data_connector in data_connectors:
            data_connector.cb_append_data_point(self.__scan_amplitude.getAIMessageBox(),self.__ai_plot_counter)
            self.__ai_plot_counter += 1
        time.sleep(0.01)
        
    def aoPlotGenerator(self, *data_connectors: tuple) -> None:
        for data_connector in data_connectors:
            data_connector.cb_append_data_point(self.__scan_amplitude.getAOMessageBox(),self.__ao_plot_counter)
            self.__ao_plot_counter += 1
        time.sleep(0.01)
    
    def __updateTask(self) -> None:
        if self.__ai_old_channel != self.__view.getAIChannel():
            self.__ai_task.createTask(self.__view.getAIChannel())
            self.__ai_task.start()
        if self.__ao_old_channel != self.__view.getAOChannel():
            self.__ao_task.createTask(self.__view.getAOChannel())
            self.__ao_task.start()
        if self.__do1_old_port != self.__view.getDO1Port() or self.__do1_old_line != self.__view.getDO1Line():
            self.__do_tasks[0].createTask(self.__view.getDO1Port(),self.__view.getDO1Line())
            self.__do_tasks[0].start()
        if self.__do2_old_port != self.__view.getDO2Port() or self.__do2_old_line != self.__view.getDO2Line():
            self.__do_tasks[1].createTask(self.__view.getDO2Port(),self.__view.getDO2Line())
            self.__do_tasks[1].start()
        
        self.__ai_old_channel = self.__view.getAIChannel()
        self.__ao_old_channel = self.__view.getAOChannel()
        self.__do1_old_port = self.__view.getDO1Port()
        self.__do1_old_line = self.__view.getDO1Line()
        self.__do2_old_port = self.__view.getDO2Port()
        self.__do2_old_line = self.__view.getDO2Line()
    
    def executeScan(self) -> None:
        self.__updateTask()
        self.__scan_amplitude.scan()
        self.doController()