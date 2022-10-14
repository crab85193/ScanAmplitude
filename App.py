import sys
import os
from turtle import update

from PyQt5.QtWidgets import QMainWindow, QApplication

from Model import Model
from View import View
from Controller import Controller

from threading import Thread

from pglive.sources.data_connector import DataConnector

class App(QMainWindow):
    """
    Main class.
    """
    def __init__(self):
        """
        Constructor.
        """
        super().__init__()
        title = "NI6212 Interface"
        width = 855
        height = 500
                
        model = Model()
        view = View(model)
        controller = Controller(model,view)
        
        Thread(target=self.task, args=(view,controller)).start()
        
        self.setWindowTitle(title)
        self.setFixedSize(width,height)
        self.setCentralWidget(view)
        self.show()
    
    
    def task(self, view: View, controller: Controller):
        ai_plot_data_connector = DataConnector(view.getPlotAI(), max_points=300, update_rate=100)
        ao_plot_data_connector = DataConnector(view.getPlotAO(), max_points=300, update_rate=100)
        
        while True:
            Thread(target=controller.executeScan()).start()
            Thread(target=controller.aiPlotGenerator,args=(ai_plot_data_connector,)).start()
            Thread(target=controller.aoPlotGenerator,args=(ao_plot_data_connector,)).start()
            # Thread(target=controller.doController).start()
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    os._exit(app.exec_())