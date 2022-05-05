from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.uic import loadUi
from datetime import *
from manage_tw import * 
from tw_search import *
from manage_tw import * 
import sys

class Dialog_Remove(QtWidgets.QDialog):
    def __init__(self,name,parent=None):
            
        super(Dialog_Remove, self).__init__(parent)
        self.setFixedWidth(352)
        self.setFixedHeight(274)
        self.name= name
        loadUi("ui/dialog_remove_ui.ui",self)
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
    
    def check_folder(self):
        """
            check_folder
        """
        self.lst_filename =os.listdir(self.nw_dir)
        if self.lst_filename ==[]:
            os.rmdir(self.nw_dir)
            self.close()
            
    def delete_file(self):
        """
            RemoveFile by path Directory
        """
        try: 
         row = self.list_remove.currentItem().text()
        except:
            row = ""
        if row != "":
            os.remove(self.nw_dir+'/'+str(row))
        
        check = "update"
        lst_keyword = []
        lst_keyword.append(self.name)
        self.ma_tw.backup_data(self.dir,lst_keyword,check)
        self.setter()
        self.check_folder()
        
"""if __name__ == "__main__":


    app  = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    app.setStyle("Fusion")
    name = "Ez"
    main = Dialog_Remove(name)
    widget.addWidget(main)
    widget.setFixedWidth(443)
    widget.setFixedHeight(401)
    widget.show()
    sys.exit(app.exec_()) """     
        
        