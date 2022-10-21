import queue
import time

from NIDAQmxController import NIDAQ_ai_task
from NIDAQmxController import NIDAQ_ao_task

class ScanAmplitude(object):
    def __init__(self, ai_task: NIDAQ_ai_task, ao_task: NIDAQ_ao_task):
        self.__ai_task = ai_task
        self.__ao_task = ao_task
    
        self.__ai_msg_box = queue.Queue(maxsize=500)
        self.__ao_msg_box = queue.Queue(maxsize=500)
        
        self.initialize()
    
    def initialize(self) -> None:
        self.__scan_state = False
        self.__threshold = 0.0
        self.__vmax = 0.0
        self.__vmin = 0.0
        self.__vinc = 0.0
        self.__slope = 1.0
        self.__vo = 0
        self.__flag = False
        
        self.__do_state = [False,False]
        self.__threshold_state = False
        self.__conditioning_state = False
                
        self.__dt = 5
        
        self.__initMessageBox()
    
    def initFlag(self) -> None:
        self.__flag = False
        self.__slope = 1.0
    
    def __initMessageBox(self) -> None:
        while not self.__ai_msg_box.empty():
            self.__ai_msg_box.get()
        while not self.__ao_msg_box.empty():
            self.__ao_msg_box.get()
    
    def getAIMessageBox(self) -> float:
        if self.isAIMessageBoxEmpty():
            return 0.0
        else:
            return self.__ai_msg_box.get()
    
    def getAOMessageBox(self) -> float:
        if self.isAOMessageBoxEmpty():
            return 0.0
        else:
            return self.__ao_msg_box.get()
        
    def isAIMessageBoxEmpty(self) -> bool:
        return self.__ai_msg_box.empty()
    
    def isAOMessageBoxEmpty(self) -> bool:
        return self.__ao_msg_box.empty()
    
    def isAIMessageBoxFull(self) -> bool:
        return self.__ai_msg_box.full()
    
    def isAOMessageBoxFull(self) -> bool:
        return self.__ao_msg_box.full()
    
    def setConditioningState(self, state: bool) -> None:
        self.__conditioning_state = state
        
    def getConditioningState(self) -> bool:
        return self.__conditioning_state
    
    def setParameters(self, scan_state: bool, threshold: float, vmax: float, vmin: float, vinc: float, do_port_use_state: float) -> None:
        self.__scan_state = scan_state
        self.__threshold = threshold
        self.__vmax = vmax
        self.__vmin = vmin
        self.__vinc = vinc
        self.__do_port_use_state = do_port_use_state
    
    def __isThreshold(self, threshold: float, vi: float) -> bool:
        if threshold > 0 and vi >= threshold or threshold < 0 and vi <= threshold:
            self.__threshold_state = True
        else:
            self.__threshold_state = False
        
        return self.__threshold_state
    
    def getThresholdState(self) -> bool:
        return self.__threshold_state
    
    def getDOState(self, do_num: int) -> bool:
        return self.__do_state[do_num]
            
    def scan(self) -> None:
        vi = self.__ai_task.getAIData_single()[0]
        
        if self.__scan_state:            
            if self.__isThreshold(self.__threshold,vi) and self.__conditioning_state and not self.__flag:
                self.__flag = True
                time.sleep(self.__dt/1000)
                
                for i in range(len(self.__do_port_use_state)):
                    self.__do_state[i] = self.__do_port_use_state[i]
                
                self.__slope = 0
            else:
                self.__vo = self.__vo + self.__slope * self.__vinc
            
            if self.__slope > 0 and self.__vinc > 0 and self.__vo >= self.__vmax or self.__vinc < 0 and self.__vo <= self.__vmin:
                self.__slope = -1.0
            
            elif self.__slope < 0 and self.__vinc > 0 and self.__vo <= self.__vmin or self.__vinc < 0 and self.__vo >= self.__vmax:
                self.__slope = 1.0
        
        self.__ao_task.setAOData(self.__vo)
        
        self.__ai_msg_box.put(vi)
        self.__ao_msg_box.put(self.__vo)