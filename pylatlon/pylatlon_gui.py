import pylatlon
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
    def __init__(self, parent=None, width=15, height=4, dpi=100,projection=ccrs.PlateCarree()):
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

    def plot(self,lon=None,lat=None):
        self.axes.cla()
        self.axes.set_global()
        self.axes.coastlines()
        if(lon is not None):
            self.axes.plot([lon],[lat],'or',transform=ccrs.PlateCarree())

        #self.axes.set_title('pylatlon')


class pylatlonWidget(QtWidgets.QWidget):
    def __init__(self,logging_level=logging.INFO):
        QtWidgets.QWidget.__init__(self)
        self.layout = QtWidgets.QGridLayout(self)


        # The widgets for entering positions
        self.input = QtWidgets.QWidget()
        self.format = QtWidgets.QWidget()
        self.input_layout = QtWidgets.QFormLayout(self.input)
        self.format_layout = QtWidgets.QFormLayout(self.format)
        self.parse_1 = QtWidgets.QPushButton('Parse')
        self.parse_1.clicked.connect(self.parse_string)
        self.layout.addWidget(self.input,0,0)
        self.layout.addWidget(self.parse_1,0,1)
        self.layout.addWidget(self.format,0,2)


        self.input1 = QtWidgets.QLineEdit()
        #self.format1 = QtWidgets.QLineEdit()
        self.format1_combo = QtWidgets.QComboBox()
        self.format1_combo.currentIndexChanged.connect(self.custom_format)
        self.layout.addWidget(self.format1_combo,0,3)
        #self.format1.setEditable(True)
        for f in pylatlon.formats:
            self.format1_combo.addItem(f)

        self.format1_combo.addItem('Custom')
        #input1.textChanged.connect(textchanged)
        self.input_layout.addRow("Position string",self.input1)
        self.format_layout.addRow("Format",self.format1_combo)

        # Add the latlon object
        self.latlabel = QtWidgets.QLabel('Latitude: ?')
        self.lonlabel = QtWidgets.QLabel('Longitude: ?')
        self.layout.addWidget(QtWidgets.QLabel('Position parsed'),1,0)
        self.layout.addWidget(self.latlabel,1,1)
        self.layout.addWidget(self.lonlabel,1,2)
        # The map to show the position
        self.map = MapCanvas(self,width=5, height=4)
        self.map_toolbar = NavigationToolbar(self.map,self)
        self.layout.addWidget(self.map,3,0,1,4)
        self.layout.addWidget(self.map_toolbar,4,0,1,4)

    def custom_format(self):
        s = self.sender()
        if(s.currentText()== 'Custom'):
            print('Adding custom format')
            text, ok = QtWidgets.QInputDialog.getText(self, 'Custom format input', 'Enter custom format:')
            if ok:
                s.addItem(str(text))

    def parse_string(self):
        print('Parse')
        format = self.format1_combo.currentText()
        if(format == 'Custom'):
            format = self.format1


        parse_string = self.input1.text()
        print('Parsing:' + parse_string + ' with format' + format)
        pos = pylatlon.latlon.strp(parse_string,format)
        if(pos is not None):
            self.latlabel.setText('Latitude: ' + str(pos.dlat))
            self.lonlabel.setText('Longitude: ' + str(pos.dlon))
            self.map.plot(pos.dlon,pos.dlat)
            self.map.draw()


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

        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(quitAction)
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
