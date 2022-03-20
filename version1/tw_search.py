from threading import Thread
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys, datetime, os, operator, functools, collections
from manage_tw import * 

class TwitterThread(QThread):
    
    """
    This class contains a signal and run method.
    An object of the signal is activated by .start() method
    and sends the results using MySignal Class instance.
    """
    def __init__(self, parent = None, keyword=""):
        super(QThread, self).__init__(parent)
        
        self.keyword = keyword
        self.ma_tw = manage_tw()
    
    def run(self):
        
        """
        Function is called when Thread is .strat().
        """
        x = self.ma_tw.main(self.keyword)
        self.ma_tw.gofile(self.keyword)
        print(x)
            