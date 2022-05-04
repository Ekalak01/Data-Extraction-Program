from multiprocessing.pool import TERMINATE
from PyQt5 import QtWidgets,QtCore,QtWebEngineWidgets
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
from dialog_update import *
from dialog_remove import *
from manager_object import *
################
import time
import datetime
from dateutil.parser import parse
from io import StringIO
###############

import queue
import threading
import time

class WebEngineView(QtWebEngineWidgets.QWebEngineView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.page().profile().downloadRequested.connect(self.onDownloadRequested)
        self.windows = []

    @QtCore.pyqtSlot(QtWebEngineWidgets.QWebEngineDownloadItem)
    def onDownloadRequested(self, download):
        if (
            download.state()
            == QtWebEngineWidgets.QWebEngineDownloadItem.DownloadRequested
        ):
            path, _ = QtWidgets.QFileDialog.getSaveFileName(
                self, self.tr("Save as"), download.path()
            )
            if path:
                download.setPath(path)
                download.accept()

    def createWindow(self, type_):
        if type_ == QtWebEngineWidgets.QWebEnginePage.WebBrowserTab:
            window = QtWidgets.QMainWindow(self)
            view = QtWebEngineWidgets.QWebEngineView(window)
            window.resize(640, 480)
            window.setCentralWidget(view)
            window.show()
            return view

    def updateChart(self, chart, **kwargs):
        output = StringIO()
        chart.save(output, "html", **kwargs)
        self.setHtml(output.getvalue())

class colck:
    
    def __init__(self,time_val):
        self.time_val = time_val
        
def singleton(cls):
    """ decorator function to implement singleton design pattern. See PEP318."""
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

@singleton
class MySignal(QObject):
    
    #Signal Class which includes a signal as class attribute.
    
    object_signal = pyqtSignal(colck)
    
class MyThreadx(QThread):
    
    """
    This class contains a signal and run method.
    An object of the signal is activated by .start() method
    and sends the results using MySignal Class instance.
    """
    def __init__(self, val):
        super().__init__()
        
        self.object_signal = MySignal().object_signal
        #print(type( self.object_signal))
        self.val = val
        
        #self.run()
        
    def run(self):
        
        """
        Function is called when Thread is .strat().
        """
        while(1):
            
            #my_id = MyObject().send_id()
            time_val = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            #print(time_val)
            self.object_signal.emit(colck(time_val))
            # Defining a ranodm sleep time (0-10) seconds.
            sleep_time = 1
            time.sleep(sleep_time)
        
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
    
    def sort(self, Ncol, order):
        self.layoutAboutToBeChanged.emit()
        header = self.arraydata.columns[Ncol]
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        try:

            for j in self._dataframe.iloc[:,Ncol]:
            
                if '-' in str(j):
                    
                    self._dataframe[header]=pd.to_datetime(self._dataframe[header].astype(str), format='%Y-%m-%d')
                    #print(self._dataframe[header])
                    self._dataframe[header] = self._dataframe[header].dt.strftime('%d/%m/%Y')
                    #print(self._dataframe[header])
                    break
                else:
                    pass
                
        except:
            pass
        
        try:
            for j in self._dataframe.iloc[:,Ncol]:
            
                if '00:00:00' in str(j):
                    
                    self._dataframe[header]=pd.to_datetime(self._dataframe[header].astype(str), dayfirst=True)
                    #print(self._dataframe[header])
                    self._dataframe[header] = self._dataframe[header].dt.strftime('%d/%m/%Y')
                    #print(self._dataframe[header])
                    break
                else:
                    pass
                
        except:
            pass
            
        for j in self._dataframe.iloc[:,Ncol]:
            if str(j) in months:
                self._dataframe[header]=pd.Categorical(self._dataframe[header], categories=months, ordered=True)
                if order == 0:
                    self._dataframe=self._dataframe.sort_values(by=header,ascending=True)
                elif order == 1:
                    self._dataframe=self._dataframe.sort_values(by=header,ascending=False)
                break
            if '/' in str(j):
                try :
                    self._dataframe[header]=pd.to_datetime(self._dataframe[header].astype(str), dayfirst=True)
                    self._dataframe[header] = self._dataframe[header].dt.strftime('%d/%m/%Y')
                except:
                    pass
                self._dataframe[header]=pd.to_datetime(self._dataframe[header].astype(str), format='%d/%m/%Y')
                if order == 0:
                    self._dataframe=self._dataframe.sort_values(by=header,ascending=True)
                    self._dataframe[header] = self._dataframe[header].dt.strftime('%d/%m/%Y')
                elif order == 1:
                    self._dataframe=self._dataframe.sort_values(by=header,ascending=False)
                    self._dataframe[header] = self._dataframe[header].dt.strftime('%d/%m/%Y')
                break

            elif type(j) == int :
                self._dataframe[header]=self._dataframe[header].astype(int)
                if order == 0:
                    self._dataframe=self._dataframe.sort_values(by=header,ascending=True)
                elif order == 1:
                    self._dataframe=self._dataframe.sort_values(by=header,ascending=False)
                break
            else:
                if order == 0:
                    self._dataframe=self._dataframe.sort_values(by=header,ascending=True)
                elif order == 1:
                    self._dataframe=self._dataframe.sort_values(by=header,ascending=False)
                break

        self.layoutChanged.emit()

class list_tweet(QtWidgets.QListWidget):
    #got_signal = pyqtSignal(str)
    def __init__(self, parent=None):
        super(list_tweet, self).__init__(parent)
        
        """self.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.setAcceptDrops(True)
        self.setViewMode(QListView.IconMode)"""
        
    def contextMenuEvent(self,event:QContextMenuEvent):
        try:
            menux = QMenu()
            itemstr=self.currentItem().text() 
            Re=menux.addAction('Remove')

            action = menux.exec_(event.globalPos())
            if action == Re:
                agg='Remove'
            self.sett.remove_file(itemstr,agg)
        except:
            pass 
        
    def setup(self,sett):
        self.sett = sett
    
class pop_main_tw(QtWidgets.QDialog):
    
    def __init__(self,parent=None):
        
        super(pop_main_tw, self).__init__(parent)
        
        self.setWindowTitle('Web Twitter')
        self.setFixedWidth(1391)
        self.setFixedHeight(743)
        loadUi("ui/main_tw_ui.ui",self)
        
        self.list_tweet.setup(self)
        self.chartmanage=Chart()
        self.my_layout=QVBoxLayout(self.chart)
        self.w = WebEngineView()
        #### Connect Button ####
        self.search_bt.clicked.connect(self.search)
        self.manual_update_bt.clicked.connect(self.search_update_manual)
        #self.wb_bt.clicked.connect(self.addsheet)
        self.ex_bt.clicked.connect(self.close_x)
        self.ma_tw = manage_tw()
        self.ma_tw.Folder_tw()
        self.dir = self.ma_tw.Folder_tw()[0]
        self.save_text = self.ma_tw.Folder_tw()[1]
        
        self.list_tweet.clicked.connect(self.gotofile)
        
        self.ma_tw.read_txt(self.dir)
        #self.lst_keyword = self.ma_tw.read_txt(self.dir)
        
        self.start_tm.setDate(QDate.currentDate())
        self.stop_tm.setDate(QDate.currentDate())
        
        self.related_bt.clicked.connect(self.related_show)
        self.dataframe_bt.clicked.connect(self.dataframe_show)
        self.statics_bt.clicked.connect(self.stat_show)
        self.export_bt.clicked.connect(self.export)
        self.relatedword_bt_.clicked.connect(self.relatedword_show)
        
        self.twitter_worker = TwitterThread(self)
        self.twitter_worker.set_search_progress.connect(self.event_set_progress)
        #self.twitter_worker.df_progress.connect(self.keep_progress)
        #self.twitter_worker.finished.connect(self.event_end_update)
        self.twitter_worker.finished.connect(self.on_finished)
        
        self.my_signal = MySignal()
        self.object_signal = self.my_signal.object_signal
        self.object_signal.connect(self.show_it)
        
        self.progressBar.hide()
        self.tableView_hastag.hide()
        self.tableView_stat.hide()
        self.tableView_word.hide()
        self.w.hide()
        
        #self.update_tw()
        #self.backdatabase()
        self.show()
        self.viewfile()
        self.openupdate()
                  
    def remove_file(self,itemstr,agg):
    
        if agg == "Remove":
            #print(itemstr)
            Remove_Popup = Dialog_Remove(itemstr)
            Remove_Popup.exec()
            self.viewfile()
        else:
            pass

    def export(self):
        try:
            start=self.set_startdatestr[::-1]
            stop=self.set_stopdatestr[::-1]
            savepath='export/'+self.tw+' '+start+' to '+stop+'.csv'
            df=self.twitter_worker.get()[0]
            df.to_csv(savepath,index=False)
        except:
            pass

    def openupdate(self):
        exPopup = Dialog_Update(self)
        #exPopup.setGeometry(100, 200, 100, 100)
        exPopup.exec()
        x = exPopup.get_update() 
        print("+++ Update +++ : ",x)
        if x == True:
            self.update_tw()
            
    def viewfile(self):
        #readfile = self.ma_tw.read_txt(self.dir)
        self.list_tweet.clear()
        self.lst_keyword = self.ma_tw.read_txt(self.dir)
        self.list_tweet.insertItems(0,self.lst_keyword)
    
    def gotofile(self,sel_item):
        
        sel_item=self.list_tweet.currentItem().text()
        get_sh = self.get_search()
        st = get_sh[1]
        sp = get_sh[2]
        dr = get_sh[3]
        self.progressBar.show()
        
        self.tw_ed.clear()
        self.tw_ed.setText(sel_item)
        status = "notupdate"
       
        
        #print(self.twitter_worker.isRunning())
        
        if self.twitter_worker.isRunning() == True :
            print("Pass")
            pass

        else:
            
            self.x = [str(sel_item),str(st),str(sp),str(dr),str(status)]
            
            self.twitter_worker.start()
            
            #self.twitter_worker.set_search_progress.connect(self.event_set_progress)
            #self.twitter_update.update_progress.connect(self.event_set_progress)
            #self.twitter_update.finished.connect(self.event_end_update)
            #self.twitter_worker.finished.connect(self.on_finished)
            
            try :
                self.addtotable(self.twitter_worker.get()[0])
            except :
                pass
            #self.progressBar.hide()
            return True
        
    def show_it(self, nval=None):
        
        my_text = f"{nval.time_val}"
        self.time.setText(my_text)
    
    def update_tw(self):
        #self.ma_tw.get_for_openprogram
        self.progressBar.show()
        self.progressBar.setValue(int(0)) 
        #self.ma_tw.write_txt(self.dir,self.save_text)
        self.currentdate = self.start_tm.date().getDate()
        self.currentdate=list(self.currentdate)
        currentdate='-'.join(str(e)for e in self.currentdate)
    
        self.lst_keyword = self.ma_tw.read_txt(self.dir)
        self.twitter_update = auto_update_tw(self,str(currentdate),self.dir,self.lst_keyword)
        self.twitter_update.start()
        self.twitter_update.update_progress.connect(self.event_set_progress)
        self.twitter_update.finished.connect(self.event_end_update)
        
    def event_set_progress(self, vals):
        self.progressBar.setValue(vals) 
    
    def event_end_update(self):
        self.viewfile()
        self.progressBar.hide()
          
    def search(self):
        self.progressBar.show()
        get_sh = self.get_search()
        tw = get_sh[0]
        st = get_sh[1]
        sp = get_sh[2]
        dr = get_sh[3]
        status = "notupdate"
        
        print(self.twitter_worker.isRunning())
        if self.twitter_worker.isRunning() == True :
            print("Pass")
            pass
        else:
            #self.twitter_worker = TwitterThread(self,tw,st,sp,dr,status)
            #self.gotofile(tw)
            
            self.x = [str(tw),str(st),str(sp),str(dr),str(status)]
            
            self.twitter_worker.start()
            
            #self.twitter_worker.start(tw,st,sp,dr,status)
            
            #self.twitter_worker.set_search_progress.connect(self.event_set_progress)
            #self.twitter_worker.df_progress.connect(self.keep_progress)
            #self.twitter_worker.finished.connect(self.event_end_update)
            #self.twitter_worker.finished.connect(self.on_finished)
            
        
    def event_end_update(self):
        self.progressBar.hide()
        
    """def keep_progress(self,df_progress):
        self.df_progress = df_progress
        return self.df_progress"""
    
    @QtCore.pyqtSlot()
    def on_finished(self):
        
        self.viewfile()
        self.op_pd()
        self.event_end_update()
        self.twitter_worker.terminate()
        print('thread finished')
        
    def get_search(self):
        
        dir = self.dir 
        
        self.tw = str(self.tw_ed.text())
        startdate=self.start_tm.date().getDate()
        startdate=list(startdate)
        self.set_startdatestr='-'.join(str(e)for e in startdate)
        
        stopdate=self.stop_tm.date().getDate()
        stopdate=list(stopdate)
        self.set_stopdatestr='-'.join(str(e)for e in stopdate)
        
        #print("start_time",set_startdatestr)
        #print("stop_time",set_stopdatestr)
        
        return [self.tw,self.set_startdatestr,self.set_stopdatestr,dir]
    
    def search_update_manual(self):
        self.progressBar.show()
        get_sh = self.get_search()
        tw = get_sh[0]
        st = get_sh[1]
        sp = get_sh[2]
        dr = get_sh[3]
        status = "update"
        #self.twitter_worker = TwitterThread()
        #self.gotofile(tw)
        
        self.x = [str(tw),str(st),str(sp),str(dr),str(status)]
            
        self.twitter_worker.start()
        
        #self.twitter_worker.start(tw,st,sp,dr,status)
        #self.twitter_worker.set_search_progress.connect(self.event_set_progress)
        #self.twitter_worker.df_progress.connect(self.keep_progress)
        #self.twitter_worker.finished.connect(self.event_end_update)
        #self.twitter_worker.finished.connect(self.on_finished)
    
    def op_pd(self):
        print("op_pd")
        try :
            #print(self.twitter_worker.get())
            self.addtotable(self.twitter_worker.get()[0])
            self.keep_statics(self.twitter_worker.get()[1])
            self.keeprelatedword(self.twitter_worker.get()[0])
        except :
            pass
        
     
    def addtotable(self,df):
        try:
            self.model = PandasModel(df)
            self.tableView.setModel(self.model)
            self.tableView.setSortingEnabled(True)
            self.tableView.sortByColumn(0, Qt.AscendingOrder)
            self.keep_related(df)
            
            self.dataframe_show()
        except:
            pass
    
    def keep_related(self,df):
        try:
            keep_re_df = self.ma_tw.releast_hastag(df)
            self.model = PandasModel(keep_re_df)
            self.tableView_hastag.setModel(self.model)
            self.tableView_hastag.setSortingEnabled(True)
            self.tableView_hastag.sortByColumn(0, Qt.AscendingOrder) 
        except:
            pass
    
    def keep_statics(self,keep_st_df):
        try:
            self.my_layout.removeWidget(self.w)
        except:
            pass
        try:
            print(keep_st_df)
            self.model = PandasModel(keep_st_df)
            self.tableView_stat.setModel(self.model)
            self.tableView_stat.setSortingEnabled(True)
            self.tableView_stat.sortByColumn(0, Qt.AscendingOrder) 
            charts=self.chartmanage.pieplot(keep_st_df)
            self.w.updateChart(charts)
            self.my_layout.addWidget(self.w)
            return keep_st_df
        except:
            pass
    
    def dataframe_show (self):
        self.tableView_stat.hide()
        self.tableView_hastag.hide()
        self.tableView_word.hide()
        self.chart.hide()
        self.w.hide()
        self.tableView.show()
    
    def related_show(self):
        self.tableView_stat.hide()
        self.tableView.hide()
        self.tableView_word.hide()
        self.chart.hide()
        self.w.hide()
        self.tableView_hastag.show()
    
    def stat_show(self):
        self.tableView_hastag.hide()
        self.tableView.hide()
        self.tableView_word.hide()
        self.chart.show()
        self.w.show()
        self.tableView_stat.show()

    def relatedword_show (self):
        self.tableView_stat.hide()
        self.chart.hide()
        self.w.hide()
        self.tableView_hastag.hide()
        self.tableView.hide()
        self.tableView_word.show()
    
    def keeprelatedword(self,df_all:pd.DataFrame):
        try:
            df=self.ma_tw.relatedword(df_all)
            self.model = PandasModel(df)
            self.tableView_word.setModel(self.model)
            self.tableView_word.setSortingEnabled(True)
            self.tableView_word.sortByColumn(0, Qt.AscendingOrder) 
        except:
            pass

    def close_x(self):
        should_save = QMessageBox.question(self, "Exit", 
                                                     "Do you want to Exit?",
                                                     defaultButton = QMessageBox.Yes)
        if should_save == QMessageBox.Yes:
            self.destroy()
        else:
            pass
