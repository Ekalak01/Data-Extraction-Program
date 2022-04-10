from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.uic import loadUi
import sys
from datetime import *
import jpg
from main_tw import * 

class Mainwindow(QtWidgets.QMainWindow):
    
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        loadUi("main.ui",self)
        
        #### ------- Connect Button ------- ####
        self.tw_bt.clicked.connect(self.tw_connect)
        #self.wb_bt.clicked.connect(self.wb_connect)
        self.ex_bt.clicked.connect(self.close_x)
        
    def tw_connect(self):
        """
            Open ui Tw 
        """
        pop = pop_main_tw(self)
        #pop.setGeometry(100,200,100,100)
        pop.show()

    def close_x(self):
        should_save = QMessageBox.question(self, "Exit", 
                                                     "Do you want to Exit?",
                                                     defaultButton = QMessageBox.Yes)
        if should_save == QMessageBox.Yes:
            sys.exit(app.exec_())
        else:
            pass
        
if __name__ == "__main__":
    
    mythread = MyThreadx(1)
    mythread.start()
    
    app  = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    app.setStyle("Fusion")
    main = Mainwindow()
    widget.addWidget(main)
    widget.setFixedWidth(443)
    widget.setFixedHeight(401)
    widget.show()
    sys.exit(app.exec_())