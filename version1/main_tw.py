from PyQt5 import QtGui, QtWidgets,QtCore,QtWebEngineWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
import pandas as pd
from PyQt5.uic import loadUi
import sys
from datetime import *
import os
import re
import shutil
import numpy as np
import random
import jpg
from manage_tw import * 
import threading
import concurrent.futures
from tw_search import *

class PandasModel(QAbstractTableModel):
    """A model to interface a Qt view with pandas dataframe """
    
    def __init__(self, dataframe: pd.DataFrame, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._dataframe = dataframe
        self.arraydata = self._dataframe
        #print(dataframe)
        #self.countheadtype(dataframe)
        
    def rowCount(self, parent=QModelIndex()) -> int:
        """ Override method from QAbstractTableModel

        Return row count of the pandas DataFrame
        """
        if parent == QModelIndex():
            return len(self._dataframe)

        return 0

    def columnCount(self, parent=QModelIndex()) -> int:
        """Override method from QAbstractTableModel

        Return column count of the pandas DataFrame
        """
        if parent == QModelIndex():
            return len(self._dataframe.columns)
        return 0

    def data(self, index: QModelIndex, role=Qt.ItemDataRole):
        """Override method from QAbstractTableModel

        Return data cell from the pandas DataFrame
        """
        if not index.isValid():
            return None

        if role == Qt.DisplayRole:
            return str(self._dataframe.iloc[index.row(), index.column()])

        return None
    
    def headerData(
        self, section: int, orientation: Qt.Orientation, role: Qt.ItemDataRole):
        """Override method from QAbstractTableModel

        Return dataframe index as vertical header data and columns as horizontal header data.
        """
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._dataframe.columns[section])

            if orientation == Qt.Vertical:
                return str(self._dataframe.index[section])

        return None
    
class pop_main_tw(QtWidgets.QDialog):
    
    def __init__(self,parent=None):
        
        super(pop_main_tw, self).__init__(parent)
        
        self.setFixedWidth(931)
        self.setFixedHeight(746)
        loadUi("main_tw_ui.ui",self)
        
        #### Connect Button ####
        self.search_bt.clicked.connect(self.search)
        #self.wb_bt.clicked.connect(self.addsheet)
        self.ex_bt.clicked.connect(self.close_x)
        self.ma_tw = manage_tw()
        self.ma_tw.Folder_tw()
    
    def search(self):
        
        tw = str(self.tw_ed.text())
        """thread1= threading.Thread(target=ma_tw.main,args=(tw,))
        thread1.start()
        print(thread1.join())"""
        self.twitter_worker = TwitterThread(self,tw)
        #self.gotofile(tw)
        self.twitter_worker.start()
        self.twitter_worker.finished.connect(self.on_finished)
    
    @QtCore.pyqtSlot()
    def on_finished(self):
        print('thread finished')
        tw = str(self.tw_ed.text())
        self.gotofile(tw)
        
    def gotofile(self,sel_item):
        
        ma = manage_tw()
        try :
            se = ma.gofile(sel_item)
            self.addtotable(se)
        except :
            pass
        return True  
     
    def addtotable(self,df):
        try:
            self.model = PandasModel(df)
            self.tableView.setModel(self.model)
            self.tableView.setSortingEnabled(True)
            self.tableView.sortByColumn(0, Qt.AscendingOrder)
        except:
            pass 

    def close_x(self):
        should_save = QMessageBox.question(self, "Exit", 
                                                     "Do you want to Exit?",
                                                     defaultButton = QMessageBox.Yes)
        if should_save == QMessageBox.Yes:
            """op = importclass()
            dr = op.opensheet()
            nt = op.save(dr)
            self.write_to_file(nt)"""
            sys.exit()
        else:
            pass
