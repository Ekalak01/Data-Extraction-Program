from threading import Thread
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.uic import loadUi
from manage_tw import * 
from crawler import * 
import datetime

class auto_update_twProgress(QDialog):
    def __init__(self,parent=None):
        
        super(auto_update_twProgress, self).__init__(parent)
        loadUi("progress.ui",self)
        self.setFixedWidth(380)
        self.setFixedHeight(517)
        """self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setGeometry(100,200,100,300)"""
        self.setWindowTitle("Filter Data")
        self.show()
        

class auto_update_tw(QThread):
    update_progress = pyqtSignal(int)
    def __init__(self, parent = None , Start = "",dir = "", lst_keyword = [] ):
        super(QThread, self).__init__(parent)
        
        self.ma_tw = manage_tw()
        self.Start_dt =  datetime.datetime.strptime(Start, "%Y-%d-%m")
        self.lst_keyword = lst_keyword
        self.Stop_count = len(self.lst_keyword)
        self.i = 0
        self.keyword = ""
        self.dir = dir
        #print(self.dir)
        """self.lst_keyword = self.ma_tw.read_txt(self.dir)"""
        
    def run(self):
        
        """
        Function is called when Thread is .strat().
        """
        """self.PopUp = auto_update_twProgress(self)
        self.PopUp.setGeometry(100, 200, 100, 100)
        self.PopUp.exec()"""
        
        counter_progress = 0
        if self.Stop_count  == 0:
            delta_day = 1
        else:
            delta_day = self.Stop_count
        percentage = (1 / delta_day) * 100
        #print(percentage)
        for self.keyword in self.lst_keyword :
            if self.i != self.Stop_count :
                if self.keyword == "" :
                        pass
                else:
                    counter_progress += int(round(percentage/2, 0))
                    self.update_progress.emit(counter_progress)
                    #if str(self.Start_dt.date())+".csv" not in self.old_data:
                    print("...Update"+"--->"+r"Date : {} / Keyword : {}".format(self.Start_dt.date(),self.keyword))
                    self.ma_tw.main_update(self.keyword,self.Start_dt.date())
                    print("...End Update"+"--->"+r"Date : {} / Keyword : {}".format(self.Start_dt.date(),self.keyword))
                    self.i += 1
                    #print(counter_progress,"before +")
                    counter_progress += int(round(percentage/2, 0))
                    #print(counter_progress,"after +")
                    self.update_progress.emit(counter_progress)
            else:
                break
        self.update_progress.emit(int(100)) 
        check = "update"
        self.ma_tw.backup_data(self.dir,self.lst_keyword,check)
        print("----END UPDATE----")
            
        """while self.i <= self.Stop_count:
            if self.keyword == "" :
                pass
            else:
            #if str(self.Start_dt.date())+".csv" not in self.old_data:
                print("Update..." + r"{}".format(self.Start_dt.date()))
                self.ma_tw.Open_program(self.keyword,str(self.Start_dt.date()))
                print("----End Update----"+ r"{}".format(self.Start_dt.date()))
                self.i += 1"""
class auto_update_wb(QThread):
    update_progress = pyqtSignal(int)
    def __init__(self, parent = None ):
        super(QThread, self).__init__(parent)
        self.craw=Crawler()
        
        
    def run(self):
        
        """
        Function is called when Thread is .strat().
        """
        print('----Updating----')
        self.craw.updatedata()