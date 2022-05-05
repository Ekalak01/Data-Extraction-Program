from threading import Thread
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import datetime
from manage_tw import * 

class queueThread(QThread):
    
    """
    This class contains a signal and run method.
    An object of the signal is activated by .start() method
    and sends the results using MySignal Class instance.
    """
    set_search_progress = pyqtSignal(int)
    
    def __init__(self, parent = None, qu = ""):
        super(QThread, self).__init__(parent)
        
        self.ma_tw = manage_tw()
        self.qu = qu
       
        
    def run(self):
        
        """
        Function is called when Thread is .strat().
        """
        
          
    def get (self):
      
        merge_dataframe = self.ma_tw.merge_df(self.list_df)
        back_dataframe  = self.ma_tw.back_df_notsave(self.list_df)
        return [merge_dataframe,back_dataframe]
    
        
            