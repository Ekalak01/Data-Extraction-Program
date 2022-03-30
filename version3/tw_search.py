from threading import Thread
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import datetime
from manage_tw import * 

class TwitterThread(QThread):
    
    """
    This class contains a signal and run method.
    An object of the signal is activated by .start() method
    and sends the results using MySignal Class instance.
    """
    set_search_progress = pyqtSignal(int)
    df_progress = pyqtSignal()
    
    def __init__(self, parent = None, keyword="",Start = "" ,Stop ="",dir = ""):
        super(QThread, self).__init__(parent)
        
        self.ma_tw = manage_tw()
        self.keyword = keyword
        self.Start_dt =  datetime.datetime.strptime(Start, "%Y-%m-%d")
        self.Stop_dt = datetime.datetime.strptime(Stop, "%Y-%m-%d")
        self.Step_dt = datetime.timedelta(days=1)
        self.Def_date = self.Stop_dt - self.Start_dt
        try:
            self.dir_inkey = os.listdir(dir + r"\{}".format(self.keyword))
        except:
            self.dir_inkey = []
        
         
        self.list_df = []
        
    def run(self):
        
        """
        Function is called when Thread is .strat().
        """
        counter_progress = 0
        if self.Def_date  == 0:
            delta_day = 1
        else:
            delta_day = self.Def_date.days + 1
        percentage = (1 / delta_day) * 100
        
        
        
        while self.Start_dt <= self.Stop_dt:
            if self.keyword == "" :
                pass
            else: 
            # มีแล้วให้ข้าม Search
                self.keyword_file = self.keyword+"-"+str(self.Start_dt.date())+".csv"    
                
                print("self.keyword_file",self.keyword_file)
                print("self.dir_inkey",self.dir_inkey)
                
                if self.keyword_file not in self.dir_inkey:
                    counter_progress += int(round(percentage/2, 0))
                    self.set_search_progress.emit(counter_progress)
                    
                    #print("Plus",self.Start_dt)
                    print("Searching..."+r"Date : {} / Keyword : {}".format(self.Start_dt.date(),self.keyword))
                    self.ma_tw.main(self.keyword,str(self.Start_dt.date()))
                    
                    self.list_df.append(self.ma_tw.gofile("{}/".format(self.keyword)+self.keyword_file))
                    self.Start_dt += self.Step_dt
                    #print(self.list_df)
                   
                    print("End..."+r"Date : {} / Keyword : {}".format(self.Start_dt.date(),self.keyword))
                    
                    
                    counter_progress += int(round(percentage/2, 0))
                    self.set_search_progress.emit(counter_progress)
                else:
                    print("___ Have File ___ : {}".format(self.keyword)+self.keyword_file)
                    #print("Plus",self.Start_dt)
                    
                    self.list_df.append(self.ma_tw.gofile("{}".format(self.keyword)+"/"+self.keyword_file))
                    self.Start_dt += self.Step_dt
                    #print(self.list_df)
                    
                    counter_progress += int(round(percentage, 0))
                    self.set_search_progress.emit(counter_progress)
                    
        """for x in range(len(list_csv)):
            xo.append(self.gofile(list_csv[x]))        
        """  
               
        self.ma_tw.merge_df(self.list_df)
        self.set_search_progress.emit(int(100))         
        print("----End While----")
        
    def get (self):
        x = self.ma_tw.merge_df(self.list_df)
        return x
    
        
            