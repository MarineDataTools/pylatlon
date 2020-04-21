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

    def plot(self,lon=None,lat=None,lon2=None,lat2=None):
        self.axes.cla()
        self.axes.set_global()
        self.axes.coastlines()
        if(lon is not None):
            print('Pos1 plot',lon,lat)
            self.axes.plot([lon],[lat],'or',transform=ccrs.PlateCarree())

        if(lon2 is not None):
            print('Pos2 plot',lon,lat)
            self.axes.plot([lon2],[lat2],'og',transform=ccrs.PlateCarree())

        #self.axes.set_title('pylatlon')


class latlonWidget(QtWidgets.QWidget):
    def __init__(self,latlon=None):
        self.latlon = latlon
        QtWidgets.QWidget.__init__(self)
        layout = QtWidgets.QVBoxLayout(self)
        # A table containing the first position
        self.postab = QtWidgets.QTableWidget()
        self.postab.setRowCount(6)
        self.postab.setColumnCount(8)
        #self.postab.setItem(1,2, QtWidgets.QTableWidgetItem("Table Cell"))
        self.postab.horizontalHeader().setVisible(False)
        self.postab.verticalHeader().setVisible(False)

        # A table containing the first position
        self.pos2tab = QtWidgets.QTableWidget()
        self.pos2tab.setRowCount(6)
        self.pos2tab.setColumnCount(8)
        #self.postab.setItem(1,2, QtWidgets.QTableWidgetItem("Table Cell"))
        self.pos2tab.horizontalHeader().setVisible(False)
        self.pos2tab.verticalHeader().setVisible(False)

        self.position_tabs = QtWidgets.QTabWidget()
        self.position_tabs.addTab(self.postab,"Position 1")
        self.position_tabs.addTab(self.pos2tab,"Position 2")
        layout.addWidget(self.position_tabs)
        # Decimal degree
        #declayout = QtWidgets.QGridLayout(self)
        #declayout.addWidget(QtWidgets.QLabel('Dec. Latitude'),0,0)
        #declayout.addWidget(QtWidgets.QLabel('Dec. Longitude'),0,1)
        #self.dlon = QtWidgets.QLabel('?')
        #self.dlat = QtWidgets.QLabel('?')
        #declayout.addWidget(self.dlat,1,0)
        #declayout.addWidget(self.dlon,1,1)
        #layout.addLayout(declayout)
    def update_position(self,latlon):
        position_table = self.position_tabs.currentWidget() # Get the current table
        if(position_table == self.postab):
            self.latlon = latlon
        elif(position_table == self.pos2tab):
            self.latlon2 = latlon

        dlonstr = '{:3.5f}'.format(abs(latlon.lon))
        dlatstr = '{:2.5f}'.format(abs(latlon.lat))
        lonstr = '{:3d}'.format(latlon.degrees_lon)
        latstr = '{:2d}'.format(latlon.degrees_lat)
        dmlonstr = '{:02.3f}'.format(latlon.dminutes_lon)
        dmlatstr = '{:02.3f}'.format(latlon.dminutes_lat)
        mlonstr = '{:02d}'.format(latlon.minutes_lon)
        mlatstr = '{:02d}'.format(latlon.minutes_lat)
        slonstr = '{:02.3f}'.format(latlon.seconds_lon)
        slatstr = '{:02.3f}'.format(latlon.seconds_lat)
        print(latlon)
        print(slonstr)
        print('slon',latlon.seconds_lon)
        print('slat',latlon.seconds_lat)
        # decimal degree
        position_table.setItem(0,0, QtWidgets.QTableWidgetItem('Lat [Dec. deg]'))
        position_table.setItem(1,0, QtWidgets.QTableWidgetItem(dlatstr))
        position_table.setItem(0,1, QtWidgets.QTableWidgetItem('Northing'))
        position_table.setItem(1,1, QtWidgets.QTableWidgetItem(latlon.northing))
        position_table.setItem(0,2, QtWidgets.QTableWidgetItem('Lon [Dec. deg]'))
        position_table.setItem(1,2, QtWidgets.QTableWidgetItem(dlonstr))
        position_table.setItem(0,3, QtWidgets.QTableWidgetItem('Easting'))
        position_table.setItem(1,3, QtWidgets.QTableWidgetItem(latlon.easting))
        # degree decimal minutes
        position_table.setItem(2,0, QtWidgets.QTableWidgetItem('Lat [Deg]'))
        position_table.setItem(3,0, QtWidgets.QTableWidgetItem(latstr))
        position_table.setItem(2,1, QtWidgets.QTableWidgetItem('Lat [Dec. min.]'))
        position_table.setItem(3,1, QtWidgets.QTableWidgetItem(dmlatstr))
        position_table.setItem(2,2, QtWidgets.QTableWidgetItem('Northing'))
        position_table.setItem(3,2, QtWidgets.QTableWidgetItem(latlon.northing))
        position_table.setItem(2,3, QtWidgets.QTableWidgetItem('Lon [Deg]'))
        position_table.setItem(3,3, QtWidgets.QTableWidgetItem(lonstr))
        position_table.setItem(2,4, QtWidgets.QTableWidgetItem('Lon [Dec. min.]'))
        position_table.setItem(3,4, QtWidgets.QTableWidgetItem(dmlonstr))
        position_table.setItem(2,5, QtWidgets.QTableWidgetItem('Easting'))
        position_table.setItem(3,5, QtWidgets.QTableWidgetItem(latlon.easting))
        # degree minutes seconds
        position_table.setItem(4,0, QtWidgets.QTableWidgetItem('Lat [Deg]'))
        position_table.setItem(5,0, QtWidgets.QTableWidgetItem(latstr))
        position_table.setItem(4,1, QtWidgets.QTableWidgetItem('Lat [Min.]'))
        position_table.setItem(5,1, QtWidgets.QTableWidgetItem(mlatstr))
        position_table.setItem(4,2, QtWidgets.QTableWidgetItem('Lat [Sec.]'))
        position_table.setItem(5,2, QtWidgets.QTableWidgetItem(slatstr))
        position_table.setItem(4,3, QtWidgets.QTableWidgetItem('Northing'))
        position_table.setItem(5,3, QtWidgets.QTableWidgetItem(latlon.northing))
        position_table.setItem(4,4, QtWidgets.QTableWidgetItem('Lon [Deg]'))
        position_table.setItem(5,4, QtWidgets.QTableWidgetItem(lonstr))
        position_table.setItem(4,5, QtWidgets.QTableWidgetItem('Lon [Min.]'))
        position_table.setItem(5,5, QtWidgets.QTableWidgetItem(mlonstr))
        position_table.setItem(4,6, QtWidgets.QTableWidgetItem('Lon [Sec.]'))
        position_table.setItem(5,6, QtWidgets.QTableWidgetItem(slonstr))
        position_table.setItem(4,7, QtWidgets.QTableWidgetItem('Easting'))
        position_table.setItem(5,7, QtWidgets.QTableWidgetItem(latlon.easting))
        # Resize
        position_table.resizeColumnsToContents()
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
        self.input1.example = False # Custom state
        self.input1.textChanged.connect(self.input_changed)
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
        self.latlon1 = latlonWidget()
        self.layout.addWidget(self.latlon1,1,0,1,4)
        #self.latlabel = QtWidgets.QLabel('Latitude: ?')
        #self.lonlabel = QtWidgets.QLabel('Longitude: ?')
        #self.layout.addWidget(QtWidgets.QLabel('Position parsed'),1,0)
        #self.layout.addWidget(self.latlabel,1,1)
        #self.layout.addWidget(self.lonlabel,1,2)
        # The map to show the position
        self.map = MapCanvas(self,width=5, height=4)
        self.map_toolbar = NavigationToolbar(self.map,self)
        self.layout.addWidget(self.map,3,0,1,4)
        self.layout.addWidget(self.map_toolbar,4,0,1,4)

    def input_changed(self):
        print('Input changed')
        #style = self.input1.getStyleSheet()
        #print(style)
        s = self.sender()
        input_str = self.input1.text()
        ind = self.format1_combo.currentIndex()
        example_str = pylatlon.formats_examples[ind]
        if(input_str == example_str):
            pass
        else: # User input, change to black
            self.input1.example = False
            self.input1.setStyleSheet("color: rgb(0, 0, 0);")
    def custom_format(self):
        s = self.sender()
        # Check if we haae an input string, if not, add an example
        input_str = self.input1.text()
        if((len(input_str) == 0)or (self.input1.example == True)):
            print('Adding an example')
            ind = s.currentIndex()
            example_str = pylatlon.formats_examples[ind]
            self.input1.setText(example_str)
            self.input1.setStyleSheet("color: rgb(255, 0, 0);")
            self.input1.example = True

        if(s.currentText()== 'Custom'):
            print('Adding custom format')
            text, ok = QtWidgets.QInputDialog.getText(self, 'Custom format input', 'Enter custom format:')
            if ok:
                s.addItem(str(text))

    def parse_string(self):
        print('Parse')
        format = self.format1_combo.currentText()
        if(format == 'Custom'):
            return

        parse_string = self.input1.text()
        print('Parsing:' + parse_string + ' with format' + format)
        pos = pylatlon.latlon.strp(parse_string,format)
        self.latlon1.update_position(pos)
        # Plotting the positions
        try:
            lon1 = self.latlon1.latlon.lon
            lat1 = self.latlon1.latlon.lat
        except Exception as e:
            print('Position1 error:' + str(e))
            lon1 = None
            lat1 = None
        try:
            lon2 = self.latlon1.latlon2.lon
            lat2 = self.latlon1.latlon2.lat
        except Exception as e:
            print('Position2 error:' + str(e))
            lon2 = None
            lat2 = None

        self.map.plot(lon1,lat1,lon2,lat2)

        self.map.draw()
        #if(pos is not None):
        #   self.map.plot(pos.lon,pos.lat)



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
