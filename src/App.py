import sys
import os
from threading import Thread
from PyQt5.QtWidgets import QMainWindow, QApplication
from pglive.sources.data_connector import DataConnector
from Model import Model
from View import View
from Controller import Controller

class App(QMainWindow):
    """
    Main class.
    """
    def __init__(self):
        """
        Constructor.
        """
        super().__init__()
        
        model = Model()
        view = View(model)
        controller = Controller(model,view)
        
        # Window Title
        title = "NI6212 Scan Amplitude"
        
        # Windows Size
        width = 855
        height = 500
        
        # Main Thread
        Thread(target=self.task, args=(view,controller)).start()
        
        self.setWindowTitle(title)
        self.setFixedSize(width,height)
        self.setCentralWidget(view)
        self.show()
    
    
    def task(self, view: View, controller: Controller) -> None:
        # Plot Data Connector
        ai_plot_data_connector = DataConnector(view.getPlotAI(), max_points=300, update_rate=100)
        ao_plot_data_connector = DataConnector(view.getPlotAO(), max_points=300, update_rate=100)
        
        while True:
            # Scan Thread
            Thread(target=controller.executeScan()).start()
            # AI Plot Thread
            Thread(target=controller.aiPlotGenerator,args=(ai_plot_data_connector,)).start()
            # AO Plot Thread
            Thread(target=controller.aoPlotGenerator,args=(ao_plot_data_connector,)).start()
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    os._exit(app.exec_())