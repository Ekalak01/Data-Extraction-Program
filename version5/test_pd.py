from PyQt5 import QtCore, QtWidgets

import pandas as pd
import numpy as np


class NumpyArrayModel(QtCore.QAbstractTableModel):
    def __init__(self, array, headers, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent=parent)
        self._array = array
        self._headers = headers
        self.r, self.c = np.shape(self.array)

    @property
    def array(self):
        return self._array

    @property
    def headers(self):
        return self._headers

    def rowCount(self, parent=QtCore.QModelIndex()):
        return self.r

    def columnCount(self, parent=QtCore.QModelIndex()):
        return self.c

    def headerData(self, p_int, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                if p_int < len(self.headers):
                    return self.headers[p_int]
            elif orientation == QtCore.Qt.Vertical:
                return p_int + 1
        return

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        row = index.row()
        column = index.column()
        if row < 0 or row >= self.rowCount():
            return None
        if column < 0 or column >= self.columnCount():
            return None
        if role == QtCore.Qt.DisplayRole:
            return float(self.array[row, column])
        return None

    def setData(self, index, value, role):
        if not index.isValid():
            return False
        if role != QtCore.Qt.EditRole:
            return False
        row = index.row()
        column = index.column()
        if row < 0 or row >= self.rowCount():
            return False
        if column < 0 or column >= self.columnCount():
            return False
        self.array.values[row][column] = value
        self.dataChanged.emit(index, index)
        return True

    def sort(self, column, order):
        self.layoutAboutToBeChanged.emit()
        argsort = self.array[:, column].argsort()
        if order == QtCore.Qt.DescendingOrder:
            argsort = argsort[::-1]
        self._array = self.array[argsort]
        self.layoutChanged.emit()
    
    


class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent=None)
        vLayout = QtWidgets.QVBoxLayout(self)
        hLayout = QtWidgets.QHBoxLayout()
        self.pathLE = QtWidgets.QLineEdit(self)
        hLayout.addWidget(self.pathLE)
        self.loadBtn = QtWidgets.QPushButton("Select File", self)
        hLayout.addWidget(self.loadBtn)
        vLayout.addLayout(hLayout)
        self.pandasTv = QtWidgets.QTableView(self)
        vLayout.addWidget(self.pandasTv)
        self.loadBtn.clicked.connect(self.loadFile)
        self.pandasTv.setSortingEnabled(True)

    def loadFile(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open File", "", "CSV Files (*.csv)"
        )
        self.pathLE.setText(fileName)
        if fileName:
            df = pd.read_csv(fileName)
            array = np.array(df.values)
            headers = df.columns.tolist()
            model = NumpyArrayModel(array, headers)
            self.pandasTv.setModel(model)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())