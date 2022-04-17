from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.uic import loadUi
from datetime import *
from manage_tw import * 
from tw_search import *
from manage_tw import * 
import shutil

class Dialog_Remove(QtWidgets.QDialog):
    def __init__(self,name,parent=None):
            
        super(Dialog_Remove, self).__init__(parent)
        self.setFixedWidth(352)
        self.setFixedHeight(274)
        self.name= name
        loadUi("dialog_remove_ui.ui",self)
        self.ma_tw = manage_tw()
        self.ma_tw.Folder_tw()
        self.dir = self.ma_tw.Folder_tw()[0]
        self.nw_dir = self.dir+"/"+name
        
        self.ok_bt.clicked.connect(self.delete_file)
        self.cel_bt.clicked.connect(self.close)
        self.setter()
        self.ok = 0
        
    def setter(self):
        self.lst_filename =self.ma_tw.remove_file(self.nw_dir)
        self.list_remove.clear()
        self.list_remove.insertItems(0,self.lst_filename)
        
    def delete_file(self):
        row = self.list_remove.currentItem().text()
        os.remove(self.nw_dir+'/'+str(row))
        self.setter()
        
    
        