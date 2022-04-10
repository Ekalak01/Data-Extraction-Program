from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
import pandas as pd
from PyQt5.uic import loadUi
import sys
from datetime import *
from manage_tw import * 
import threading
from tw_search import *
from auto_update import * 
#from main_tw import * 
class Dialog_Update(QtWidgets.QDialog):
    
    def __init__(self,parent=None):
        
        super(Dialog_Update, self).__init__(parent)
        
        self.setFixedWidth(352)
        self.setFixedHeight(274)
        loadUi("dialog_update_ui.ui",self)
        self.okButton.clicked.connect(self.ok_bt)
        self.cancelButton.clicked.connect(self.close_x)
        self.ok = 0
        self.cl = 0
        
    def ok_bt(self):
        self.ok += 1
        self.get_update()
    
    def close_x(self):
        self.cl += 0
        self.get_update()
        
    def get_update(self):
        if self.ok == 1:
            self.close()
            return True
        elif self.cl == 0:
            self.close()
            return False
        
    
        