import queue
import time

from NIDAQmxController import NIDAQ_ai_task
from NIDAQmxController import NIDAQ_ao_task
from NIDAQmxController import NIDAQ_do_task

class ScanAmplitude(object):
    def __init__(self, ai_task: NIDAQ_ai_task, ao_task: NIDAQ_ao_task, do_tasks: list):
        self.ai_task = ai_task
        self.ao_task = ao_task
        self.do_tasks = do_tasks
    
        self.ai_msg_box = queue.Queue(maxsize=500)
        self.ao_msg_box = queue.Queue(maxsize=500)
        
        self.initialize()
    
    def initialize(self):
        self.scan_state = False
        self.threshold = 0.0
        self.vmax = 0.0
        self.vmin = 0.0
        self.vinc = 0.0
        self.slope = 1.0
        self.vo = 0
        
        self.do_state = [False,False]
        self.threshold_state = False
        self.conditioning_state = False
        self.flag = False
        
        self.initMessageBox()
    
    def initMessageBox(self):
        while not self.ai_msg_box.empty():
            self.ai_msg_box.get()
        while not self.ao_msg_box.empty():
            self.ao_msg_box.get()
    
    def setAIPort(self, port: str) -> None:
        pass
    
    def setAOPort(self, port: str) -> None:
        pass
    
    def setDOPort(self, line: str, port: str) -> None:
        pass
    
    def taskStart(self):
        self.ai_task.start()
        self.ao_task.start()
        for do_task in self.do_tasks:
            do_task.start()
            do_task.setDOData(False)
        print(f'Task Start')
    
    def taskStop(self):
        self.ai_task.stop()
        self.ao_task.stop()
        for do_task in self.do_tasks:
            do_task.stop()
        print(f'Task Stop')
        
    def getAIMessageBox(self):
        if self.isAIMessageBoxEmpty():
            return 0
        else:
            return self.ai_msg_box.get()
    
    def getAOMessageBox(self):
        if self.isAOMessageBoxEmpty():
            return 0
        else:
            return self.ao_msg_box.get()
        
    def isAIMessageBoxEmpty(self):
        return self.ai_msg_box.empty()
    
    def isAOMessageBoxEmpty(self):
        return self.ao_msg_box.empty()
    
    def isAIMessageBoxFull(self):
        return self.ai_msg_box.full()
    
    def isAOMessageBoxFull(self):
        return self.ao_msg_box.full()
    
    def setConditioningState(self,state):
        self.conditioning_state = state
        
    def getConditioningState(self):
        return self.conditioning_state
    
    def setParameters(self,scan_state: bool,threshold: float,vmax: float,vmin: float,vinc: float,do_port_use_state: float):
        self.scan_state = scan_state
        self.threshold = threshold
        self.vmax = vmax
        self.vmin = vmin
        self.vinc = vinc
        self.do_port_use_state = do_port_use_state
    
    def isThreshold(self,threshold,vi):
        if threshold > 0 and vi >= threshold or threshold < 0 and vi <= threshold:
            self.threshold_state = True
        else:
            self.threshold_state = False
            
        return self.threshold_state
    
    def getThresholdState(self):
        return self.threshold_state
    
    def scan(self):
        dt = 5
        old_state = False
        
        while True:
            vi = self.ai_task.getAIData_single()[0]
            
            if old_state != self.scan_state:
                self.slope = 1.0
                print(old_state)
            
            if self.scan_state:            
                self.vo = self.vo + self.slope * self.vinc
                
                if self.isThreshold(self.threshold,vi) and self.conditioning_state and not self.flag:
                    self.flag = True
                    time.sleep(dt/1000)
                    for i in range(len(self.do_port_use_state)):
                        self.do_task[i].setDOData(self.do_port_use_state[i])
                        self.do_state[i] = self.do_port_use_state[i]
                    self.slope = 0
                    print(self.vo)
                elif self.isThreshold(self.threshold,vi):
                    pass
                
                    
                if self.slope > 0 and self.vinc > 0 and self.vo > self.vmax or self.vinc < 0 and self.vo < self.vmin:
                    self.slope = -1.0
                elif self.slope < 0 and self.vinc > 0 and self.vo < self.vmin or self.vinc < 0 and self.vo > self.vmax:
                    self.slope = 1.0
            
            self.ao_task.setAOData(self.vo)
            
            self.ai_msg_box.put(vi)
            self.ao_msg_box.put(self.vo)
            
            old_state = self.scan_state