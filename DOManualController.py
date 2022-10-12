class DOManualController(object):
    def __init__(self,do_tasks):
        self.do_tasks = do_tasks
        
    def setDOState(self,do_num,state):
        self.do_tasks[do_num].setDOData(state)
        
    def getDOState(self,do_num):
        return self.do_state[do_num]