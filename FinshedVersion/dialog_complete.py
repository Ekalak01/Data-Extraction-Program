from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
import pandas as pd
from PyQt5.uic import loadUi
import sys
#from main_tw import * 
class Dialog_Complete(QtWidgets.QDialog):
    
    def __init__(self,parent=None):
        
        super(Dialog_Complete, self).__init__(parent)
        
        self.setWindowTitle('Export')
        self.setFixedWidth(417)
        self.setFixedHeight(232)
        loadUi("ui/dialog_complete_ui.ui",self)
        self.ex_bt.clicked.connect(self.close)
        
        
    
        