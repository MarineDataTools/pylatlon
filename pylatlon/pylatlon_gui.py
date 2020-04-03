from pycnv import pycnv, pycnv_sum_folder
import sys
import os
import logging
import cartopy
import cartopy.crs as ccrs
from cartopy.io import shapereader
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np

try:
    from PyQt5 import QtCore, QtGui, QtWidgets
except:
    from qtpy import QtCore, QtGui, QtWidgets



class MapCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100,projection=ccrs.PlateCarree()):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.figwidget = fig
        self.axes = fig.add_subplot(111,projection=ccrs.Mercator())

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QtWidgets.QSizePolicy.Expanding,
                QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()

    def plot(self):
        self.axes.cla()
        self.axes.set_global()
        self.axes.coastlines()
        self.axes.plot([20.0],[54.0],'or',transform=ccrs.PlateCarree())
        self.axes.set_title('pylatlon')




class pylatlonWidget(QtWidgets.QWidget):
    def __init__(self,logging_level=logging.INFO):
        QtWidgets.QWidget.__init__(self)
        self.layout = QtWidgets.QGridLayout(self)
        #self.map_widget = QtWidgets.QWidget()
        self.map = MapCanvas(self,width=5, height=4)
        self.map_toolbar = NavigationToolbar(self.map,self)
        self.layout.addWidget(self.map,0,0)
        self.layout.addWidget(self.map_toolbar,1,0)

class pylatlonMainWindow(QtWidgets.QMainWindow):
    def __init__(self,logging_level=logging.INFO):
        QtWidgets.QMainWindow.__init__(self)
        mainMenu = self.menuBar()
        self.setWindowTitle("pylatlon")
        self.mainwidget = pylatlonWidget()
        self.setCentralWidget(self.mainwidget)
        quitAction = QtWidgets.QAction("&Quit", self)
        quitAction.setShortcut("Ctrl+Q")
        quitAction.setStatusTip('Closing the program')
        quitAction.triggered.connect(self.close_application)
        self.statusBar()

    def close_application(self):
        sys.exit()

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = pylatlonMainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
