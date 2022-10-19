class DOManualController(object):
    def __init__(self, do_tasks: list):
        self.__do_tasks = do_tasks
        self.__do_state = [False] * len(do_tasks)
        
    def setDOState(self,do_num,state):
        self.__do_tasks[do_num].setDOData(state)
        
    def getDOState(self,do_num):
        return self.__do_state[do_num]