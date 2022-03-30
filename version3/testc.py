from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.uic import loadUi
import sys
from datetime import *
import jpg
from main_tw import * 

class Mainwindow(QtWidgets.QDialog):
    
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        loadUi("progress.ui",self)
        widget.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        widget.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        widget.setGeometry(100,200,100,300)
        
    def tw_connect(self):
        """
            Open ui Tw 
        """
        pop = pop_main_tw(self)
        pop.setGeometry(100,200,100,100)
        pop.exec()

    def close_x(self):
        should_save = QMessageBox.question(self, "Exit", 
                                                     "Do you want to Exit?",
                                                     defaultButton = QMessageBox.Yes)
        if should_save == QMessageBox.Yes:
            sys.exit(app.exec_())
        else:
            pass
        
if __name__ == "__main__":
    
    
    app  = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    app.setStyle("Fusion")
    main = Mainwindow()
    widget.addWidget(main)
    widget.setFixedWidth(436)
    widget.setFixedHeight(195)
    widget.show()
    sys.exit(app.exec_())