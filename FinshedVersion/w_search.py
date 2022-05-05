from threading import Thread
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys, datetime, os, operator, functools, collections
from crawler import * 
from manager_object import *

class get_data(QThread):
    update_progress = pyqtSignal(int)
    def __init__(self, parent = None,link="",path="" ):
        super(QThread, self).__init__(parent)
        self.craw=Crawler()
        self.link=link
        self.path=path
        
    def run(self):
        
        """
        Function is called when Thread is .strat().
        """
        self.craw.getdata(self.link,self.path)

class WebThread(QThread):
    
    """
    This class contains a signal and run method.
    An object of the signal is activated by .start() method
    and sends the results using MySignal Class instance.
    """
    set_search_progress = pyqtSignal(int)
    
    def __init__(self, parent = None, keyword="",Start = "" ,Stop =""):
        super(QThread, self).__init__(parent)
        
        self.dfmanage=Dfmanage()
        self.craw = Crawler()
        self.Start_dt =  datetime.datetime.strptime(Start, "%Y-%m-%d")
        self.Stop_dt = datetime.datetime.strptime(Stop, "%Y-%m-%d")
        self.Step_dt = datetime.timedelta(days=1)
        self.Def_date = self.Stop_dt - self.Start_dt
        self.fmanage=Filemanage()
        self.keyword = keyword
        self.lst=[]
        self.dfmergelist=[]
    def run(self):
        
        """
        Function is called when Thread is .strat().
        """
        if self.keyword == "" :
            pass
        else:
            print(self.keyword)
            path=self.fmanage.createsearchfolder(self.keyword)
            counter_progress = 0
            if self.Def_date  == 0:
                delta_day = 1
            else:
                delta_day = self.Def_date.days + 1
            percentage = (1 / delta_day) * 100
            while self.Start_dt <= self.Stop_dt:
                counter_progress += int(round(percentage/2, 0))
                self.set_search_progress.emit(counter_progress)
                self.dfmergelist.append(self.craw.loaddata(path,self.keyword,self.Start_dt))
                self.Start_dt += self.Step_dt
                counter_progress += int(round(percentage/2, 0))
                self.set_search_progress.emit(counter_progress)
            self.set_search_progress.emit(int(100))
            self.dfmanage.back_df_notkeep(self.dfmergelist)
            
            print("----End While----")

        

    def get (self):
        #print(self.dfmergelist)
        #print(self.lst)
        merge_dataframe = self.dfmanage.merge_df(self.dfmergelist)
        back_dataframe  = self.dfmanage.back_df_notkeep(self.dfmergelist)
        return [merge_dataframe,back_dataframe ] 
    
    