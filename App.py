import sys
import os

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
        
        self.setWindowTitle(title)
        self.setFixedSize(width,height)
        
        model = Model()
        view = View(model)
        controller = Controller(model,view)
        
        ai_plot_data_connector = DataConnector(view.getPlotAI(), max_points=500)
        ao_plot_data_connector = DataConnector(view.getPlotAO(), max_points=500)
        Thread(target=controller.scan_amplitude.scan).start()
        Thread(target=controller.aiPlotGenerator, args=(ai_plot_data_connector,)).start()
        Thread(target=controller.aoPlotGenerator, args=(ao_plot_data_connector,)).start()
        Thread(target=controller.doController).start()
        
        self.setCentralWidget(view)
        self.show()
    
    def exec_(self):
        return 0
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    os._exit(ex.exec_() + app.exec_())