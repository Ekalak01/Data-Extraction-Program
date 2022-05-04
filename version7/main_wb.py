from multiprocessing.pool import TERMINATE
from PyQt5 import QtWidgets,QtCore,QtWebEngineWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
import pandas as pd
from PyQt5.uic import loadUi
import sys
from datetime import * 
import threading
from manager_object import *
from w_search import *
from auto_update import *
from dialog_remove_wb import *
from crawler import *
from dialog_complete import *
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
        
###############

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
        header=self.arraydata.columns[Ncol]
        try:

            for j in self._dataframe.iloc[:,Ncol]:
            
                if '-' in str(j) and '*' not in str(j):
                    
                    self._dataframe[header]=pd.to_datetime(self._dataframe[header].astype(str), format='%Y-%m-%d')
                    print(self._dataframe[header])
                    self._dataframe[header] = self._dataframe[header].dt.strftime('%d/%m/%Y')
                    print(self._dataframe[header])
                    break
                else:
                    pass
                
        except:
            pass
        
        try:
            for j in self._dataframe.iloc[:,Ncol]:
                if '00:00:00' in str(j):
                    self._dataframe[header]=pd.to_datetime(self._dataframe[header].astype(str), dayfirst=True)
                    print(self._dataframe[header])
                    self._dataframe[header] = self._dataframe[header].dt.strftime('%d/%m/%Y')
                    print(self._dataframe[header])
                    break
                else:
                    pass
                
        except:
            pass
            
        for j in self._dataframe.iloc[:,Ncol]:
            if '/' in str(j) and '*' not in str(j) :
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

class list_kw(QtWidgets.QListWidget):
    def __init__(self, parent=None):
        super(list_kw, self).__init__(parent)
        
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

class pop_main_wb(QtWidgets.QDialog):
    
    def __init__(self,parent=None):
        super(pop_main_wb, self).__init__(parent)

        self.setWindowTitle('Web Scraping')
        self.setFixedWidth(1391)
        self.setFixedHeight(743)

        loadUi("ui/main_wb_ui.ui",self)

        self.craw=Crawler()
        self.fmanage=Filemanage()
        self.dfmanage=Dfmanage()
        self.my_signal = MySignal()
        self.update_wb=auto_update_wb()
        self.chartmanage=Chart()
        self.my_layout=QVBoxLayout(self.chart)
        self.w = WebEngineView()
        self.list_kw.setup(self)

        self.start_tm.setDate(QDate.currentDate())
        self.stop_tm.setDate(QDate.currentDate())
        
        self.object_signal = self.my_signal.object_signal
        self.object_signal.connect(self.show_it)

        self.update_data()
        self.progressBar.hide()
        self.viewfile()
        self.static()

        self.w.hide()
        self.tableView_stat.hide()
        self.tableView_ref.hide()
        self.tableView_word.hide()
        self.ex_bt.clicked.connect(self.close_x)
        self.search_bt.clicked.connect(self.search)
        self.stat_bt.clicked.connect(self.stat_show)
        self.df_bt.clicked.connect(self.dataframe_show)
        self.ref_bt.clicked.connect(self.reflink_show)
        self.relatedword_bt_.clicked.connect(self.relatedword_show)
        self.export_bt.clicked.connect(self.export)
        self.list_kw.itemDoubleClicked.connect(self.selectkeyword)
        #self.list_kw.clicked.connect(self.selectkeyword)


    def reflink_show(self):
        self.tableView.hide()
        self.tableView_2.hide()
        self.chart.hide()
        self.tableView_word.hide()
        self.w.hide()
        self.tableView_stat.hide()
        self.tableView_ref.show()

    def stat_show(self):
        self.tableView.hide()
        self.tableView_2.hide()
        self.tableView_word.hide()
        self.chart.show()
        self.tableView_ref.hide()
        self.w.show()
        self.tableView_stat.show()

    def dataframe_show (self):
        self.tableView_stat.hide()
        self.chart.hide()
        self.tableView_word.hide()
        self.w.hide()
        self.tableView_2.hide()
        self.tableView_ref.hide()
        self.tableView.show() 

    def relatedword_show (self):
        self.tableView_stat.hide()
        self.chart.hide()
        self.w.hide()
        self.tableView_2.hide()
        self.tableView_ref.hide()
        self.tableView.hide() 
        self.tableView_word.show()

    def export(self):
        try:
            start=self.set_startdatestr[::-1]
            stop=self.set_stopdatestr[::-1]
            savepath='export/'+self.sel_item+' '+start+' to '+stop+'.csv'
            df=self.web_worker.get()[0]
            df.to_csv(savepath,index=False)
            Update_Popup = Dialog_Update()
            Update_Popup.exec()
        except:
            pass


    def static(self):
        self.fmanage.static()


    def remove_file(self,itemstr,agg):
        if agg == "Remove":
            print(itemstr)
            Remove_Popup = Dialog_Remove(itemstr)
            Remove_Popup.exec()
            self.viewfile()
            self.tableView.hide()
            self.tableView_stat.hide()
            self.tableView_2.show()
        else:
            pass

    def viewfile(self):
        self.list_kw.clear()
        self.lst_keyword = self.fmanage.listofkeyword()
        self.list_kw.insertItems(0,self.lst_keyword)

    def selectkeyword(self):
        self.sel_item=self.list_kw.currentItem().text()

        self.wb_ed.clear()
        self.wb_ed.setText(self.sel_item)

        path=self.fmanage.createsearchfolder(self.sel_item)
        df=self.craw.getdataindir(path)
        startdate=self.start_tm.date().getDate()
        startdate=list(startdate)
        self.set_startdatestr='-'.join(str(e)for e in startdate)
        stopdate=self.stop_tm.date().getDate()
        stopdate=list(stopdate)
        self.set_stopdatestr='-'.join(str(e)for e in stopdate)

        self.web_worker = WebThread(self,self.sel_item,self.set_startdatestr,self.set_stopdatestr)
        self.web_worker.start()
        self.progressBar.show()
        self.web_worker.set_search_progress.connect(self.event_set_progress)
        self.web_worker.finished.connect(self.on_finished)


    def update_data(self):
        self.update_wb.start()
        self.update_wb.finished.connect(self.updatefinished)

    @QtCore.pyqtSlot()
    def updatefinished(self):
        print('----Update Finished----')

    def event_set_progress(self, vals):
        self.progressBar.setValue(vals) 

    def show_it(self, nval=None):
        
        my_text = f"{nval.time_val}"
        self.time.setText(my_text)

    def get_search(self):
        keyword=str(self.wb_ed.text())
        keyword=keyword.lower()
        startdate=self.start_tm.date().getDate()
        startdate=list(startdate)
        set_startdatestr='-'.join(str(e)for e in startdate)
        
        stopdate=self.stop_tm.date().getDate()
        stopdate=list(stopdate)
        set_stopdatestr='-'.join(str(e)for e in stopdate)
        
        print("start_time",set_startdatestr)
        print("stop_time",set_stopdatestr)

        return [keyword,set_startdatestr,set_stopdatestr]
    
    def search(self):
        
        get_sh = self.get_search()
        kw = get_sh[0]
        st = get_sh[1]
        sp = get_sh[2]
        
        self.web_worker = WebThread(self,kw,st,sp)
        self.web_worker.start()
        self.progressBar.show()
        self.web_worker.set_search_progress.connect(self.event_set_progress)
        self.web_worker.finished.connect(self.on_finished)
        
    
    @QtCore.pyqtSlot()
    def on_finished(self):
        
        print('thread finished')
        dfx=self.web_worker.get()
        self.op_pd(dfx)
        self.viewfile()
        self.progressBar.hide()
    
    def op_pd(self,df):
        try: 
            self.addtotable(df[0])
            self.keep_statics(df[1])
            self.keepreflinks(df[0])
            self.keeprelatedword(df[0])
        except:
            pass
        return True
        

    def keepreflinks(self,df_all):
        try:
            df=self.dfmanage.reflinks(df_all)
            self.model = PandasModel(df)
            self.tableView_ref.setModel(self.model)
            self.tableView_ref.setSortingEnabled(True)
            self.tableView_ref.sortByColumn(0, Qt.AscendingOrder) 
            return df_all
        except:
            pass
    
    def keeprelatedword(self,df_all:pd.DataFrame):
        try:
            df=self.dfmanage.relatedword(df_all)
            self.model = PandasModel(df)
            self.tableView_word.setModel(self.model)
            self.tableView_word.setSortingEnabled(True)
            self.tableView_word.sortByColumn(0, Qt.AscendingOrder) 
        except:
            pass

    def addtotable(self,df):
        try:
            self.model = PandasModel(df)
            self.tableView.setModel(self.model)
            self.tableView.setSortingEnabled(True)
            self.dataframe_show()
        except:
            pass 
    
    def keep_statics(self,keep_st_df):
        try:
            self.my_layout.removeWidget(self.w)
        except:
            pass
        try:
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

    def close_x(self):
        should_save = QMessageBox.question(self, "Exit", 
                                                     "Do you want to Exit?",
                                                     defaultButton = QMessageBox.Yes)
        if should_save == QMessageBox.Yes:
            self.destroy()
        
        else:
            pass

    
"""if __name__ == "__main__":
    app  = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    app.setStyle("Fusion")
    main = Mainwindow()
    widget.addWidget(main)
    widget.setFixedWidth(1391)
    widget.setFixedHeight(746)
    widget.show()
    sys.exit(app.exec_())"""