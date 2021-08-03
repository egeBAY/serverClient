import sys
import sqlite3
import socket
import threading
import json
import gmplot
import random

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QAction, QLabel,QMainWindow, QVBoxLayout,QWidget
from PyQt5.QtGui import QPixmap, QMovie
from PyQt5.QtCore import Qt,QTimer,pyqtSignal
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *


class Window(QtWidgets.QWidget):
    
    def __init__(self):

       super().__init__()
       
       self.baglan()
       self.init_ui() 
       self.setFixedSize(800, 550)
       
       
    def baglan(self):
        baglanti = sqlite3.connect("database.db")

        self.cursor = baglanti.cursor()
        self.cursor.execute("Create Table If not exists users (userID TEXT, password TEXT)")

        baglanti.commit()

    def openLogginPage(self):

        server_client = Menu()
        widget.addWidget(server_client)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def init_ui(self):
       self.label = QLabel(self)
       self.label.setGeometry(QtCore.QRect(0, 0, 800, 550))
       self.label.setPixmap(QPixmap('gps.jpg'))
       
       self.label.setScaledContents(True)

       self.userID = QtWidgets.QLineEdit()
       self.userID.setPlaceholderText("Kullanici adinizi giriniz")
       self.password = QtWidgets.QLineEdit()
       self.password.setPlaceholderText("Sifrenizi giriniz")
       self.password.setEchoMode(QtWidgets.QLineEdit.Password)
       self.loginButton = QtWidgets.QPushButton("Giris Yap")
       self.textSpace = QtWidgets.QLabel("")



       v_box = QtWidgets.QVBoxLayout()

       v_box.addWidget(self.userID)
       v_box.addWidget(self.password)
       v_box.addWidget(self.textSpace)
       v_box.addStretch()
       v_box.addWidget(self.loginButton)

       h_box = QtWidgets.QHBoxLayout()

       h_box.addStretch()
       h_box.addLayout(v_box)
       h_box.addStretch()
       
       
       
       self.setLayout(h_box)
    
    
    
        
       
       
       
       self.loginButton.setShortcut("Return")

       self.loginButton.clicked.connect(self.login)
       #self.buttonDelete.clicked.connect(self.click)
       

    def login(self):

        name = self.userID.text()
        par = self.password.text()

        self.cursor.execute("Select * From users where userID = ? and password = ?", (name,par))

        data = self.cursor.fetchall()

        if len(data) == 0:
            self.textSpace.setText("Yanlis Giris\nTekrar Deneyin!!!")
        else:
            self.textSpace.setText("Giris Basarili Selam {}".format(name))
            self.loading_page = LoadingScreen()  
            self.openLogginPage()

class LoadingScreen(QWidget):

    def __init__(self):
        
        super().__init__()

        self.setFixedSize(64,64)

        self.label_animation = QLabel(self)

        self.movie = QMovie("world.gif")
        self.label_animation.setMovie(self.movie)

        timer = QTimer(self)
        self.movie.start()
        timer.singleShot(2000, self.stopGif)

        self.show()

    def stopGif(self):
        
        self.movie.stop()
        self.close()

class LoggedIn(QWidget):

    progress = pyqtSignal(str)
    progress2 = pyqtSignal(float,float)

    def __init__(self):

        super().__init__()
        
        self.init_ui()
        self.text = ""
        self.flag = 0
        self.flag2 = 0
        self.flag3 = 0
        
        self.i = 0
        self.checklist = [0,0]
        #self.connectServer()
        self.connectClient("iptal")

    def connectServer(self) -> None:
        #host = "172.16.60.231"
        host = socket.gethostbyname(socket.gethostname())
        port = 1024
        format = 'utf-8'

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((host, port))
        
        while True:
            data, addr = sock.recvfrom(2048)
            print(str(data))
            msgServer = "Coming from UDP Server".encode(format)
            sock.sendto(msgServer, addr)

    def connectClient(self, msg):
        host =  "172.16.60.231" 
        #host= socket.gethostbyname(socket.gethostname())
        port = 1024
        format = 'utf-8'

 
        if self.flag == 0:
            client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
            t1 = threading.Timer(3,self.connectClient,args=(msg,))
            t1.daemon = True
            t1.start()
           
            client_sock.sendto(msg.encode(format), (host, port))
            
            data, addr = client_sock.recvfrom(2048)
            
            print("From Server1: {}".format(str(data)))

            self.text = str(data)+"\n"+self.text
            self.progress.emit(self.text)
            
            
            coordinate_list = data.decode('utf-8').strip(')(').split(', ')
            cordinateX = float(coordinate_list[0])
            cordinateY = float(coordinate_list[1])
            self.lats, self.longs = cordinateX, cordinateY
            
            self.progress2.emit(self.lats,self.longs)
            
            if self.flag2 == 1:
                self.progress.connect(self.received_text.setPlainText)
            if self.flag3 == 1:
                """
                self.lats, self.longs = zip(
                *[(39.766706+self.i, 30.525631+self.i), (39.616830811910624, 30.616830811910624),
                  (39.546461511615+self.i, 30.5651151531+self.i)])
                """
                
                self.progress2.connect(self.draw_marker)
                #self.draw_marker()
                
                
            client_sock.close()
            
        self.flag=0

    def connectClient_2(self, msg) -> None:
        host = "172.16.60.231"
        #host = socket.gethostbyname(socket.gethostname())
        port = 1024
        format = 'utf-8'
        #serverText = serverUi()

        client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        client_sock.sendto(msg.encode(format), (host, port))
        
        data, addr = client_sock.recvfrom(2048)
        print("From Server2: {}".format(str(data)))
        self.connectClient("iptal")


    def init_ui(self):

        self.sendingText = QtWidgets.QTextEdit()
        self.sendButton = QtWidgets.QPushButton("GONDER")
        self.deleteButton = QtWidgets.QPushButton("TEMIZLE")
        self.serverButton = QtWidgets.QPushButton("SERVER")
        self.mapButton = QtWidgets.QPushButton("MAP")

        v_box = QtWidgets.QVBoxLayout()

        v_box.addWidget(self.sendingText)
        v_box.addWidget(self.sendButton)
        v_box.addWidget(self.deleteButton)
        v_box.addWidget(self.serverButton)
        v_box.addWidget(self.mapButton)

        self.deleteButton.clicked.connect(self.click)
        self.sendButton.clicked.connect(self.click)
        self.serverButton.clicked.connect(self.click)
        self.mapButton.clicked.connect(self.click)

        self.setLayout(v_box)
   
    def init_server_ui(self):

        self.received_text = QtWidgets.QTextEdit()
        self.deleteTextButton = QtWidgets.QPushButton("CLEAR")

        v_box = QtWidgets.QVBoxLayout()
        v_box.addWidget(self.received_text)
        v_box.addWidget(self.deleteTextButton)

        self.deleteTextButton.clicked.connect(self.click)
        
        self.setLayout(v_box)

    def click(self):

        sender = self.sender()

        if sender.text() == "TEMIZLE":
            self.sendingText.clear()
        elif sender.text() == "CLEAR":
            self.received_text.clear()
        elif sender.text() == "GONDER":
            print("Server'a {} gönderildi.".format(self.sendingText.toPlainText()))
            self.connectClient_2(self.sendingText.toPlainText())
            self.flag = 1
        elif sender.text() == "MAP":
            self.maxMarker = 0
            

            self.page2 = QtWidgets.QWidget()
            widget.addWidget(self.page2)
            #widget.addWidget(Map())

            widget.setCurrentIndex(widget.currentIndex() + 1)
            self.setWindowTitle('Map')
            self.window_width, self.window_height = 800, 550
            self.setMinimumSize(self.window_width, self.window_height)
            self.updateButton = QPushButton("Update",self.page2)
            self.backButton = QPushButton("Back",self.page2)
            
            

            layout = QVBoxLayout(self.page2)
            layout.addWidget(self.updateButton)
            layout.addWidget(self.backButton)
            #self.setLayout(layout)

            #coordinate = received_coordinates.connectClient("").decode('utf-8')
            #coordinate_list = coordinate.strip(')(').split(', ')
            #cordinateX = float(coordinate_list[0])
            #cordinateY = float(coordinate_list[1])

            #print(cordinateX, cordinateY)
            #self.m = folium.Map(
                #tiles='Stamen Terrain',
                #zoom_start=13,
                #location=(39.766706, 30.525631)

            #)

            #self.draw_marker()

            # save map data to data object
            #self.data1 = io.BytesIO()
            #self.m.save(self.data1, close_file=False)

            self.webView = QWebEngineView()
            self.webView.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
            self.webView.load(QUrl.fromLocalFile(
                QDir.current().absoluteFilePath('geomap.html')))
            #self.webView.setHtml(self.data1.getvalue().decode())
            layout.addWidget(self.webView)
            
            self.gmap = gmplot.GoogleMapPlotter(
                39, 30, 6, apikey='AIzaSyDpgKJ3LZciHRNcrHQoVdgbWRgim_Y5jU0')
        
            self.webView.reload()
            
            self.flag3 = 1
            self.updateButton.clicked.connect(self.update)
            self.backButton.clicked.connect(self.clickServerUi)
            #m = Map()
            #widget.addWidget(m)
            #widget.setCurrentIndex(widget.currentIndex() + 1)

        else:

            self.page = QtWidgets.QWidget()
            self.received_text = QtWidgets.QTextEdit(self.page)
            self.deleteTextButton = QtWidgets.QPushButton("CLEAR", self.page)
            self.clientButton = QtWidgets.QPushButton("CLIENT", self.page)

            v_box = QtWidgets.QVBoxLayout(self.page)
            v_box.addWidget(self.received_text)
            v_box.addWidget(self.deleteTextButton)
            v_box.addWidget(self.clientButton)

            self.deleteTextButton.clicked.connect(self.clickServerUi)
            self.clientButton.clicked.connect(self.clickServerUi)

            #self.received_text.setPlainText(data.decode('utf-8'))
            self.update_serverText(b'Server:')
            #self.progress.connect(self.update_serverText)

            #self.setLayout(v_box)
            widget.addWidget(self.page)

            widget.setCurrentIndex(widget.currentIndex() + 1)
            #self.init_server_ui()
            self.flag2 = 1
    def update(self):
        self.webView.reload()
        

    def update_serverText(self, text):

            self.received_text.setPlainText(text.decode('utf-8'))

    def clickServerUi(self):

        senderSrv = self.sender()

        if senderSrv.text() == "CLEAR":
            self.received_text.clear()
        else:
            widget.addWidget(LoggedIn())
            widget.setCurrentIndex(widget.currentIndex() + 1)

    def draw_marker(self,x,y):
        
        self.lats=x
        self.longs=y
        #self.webView.repaint()
        
        
        
        """    
        with open('coordinates.json') as file:
            coordinates = json.load(file)
            print(coordinates)

        for values in coordinates['coordinates']:
            coordinateX = values['xValue']
            coordinateY = values['yValue']
        """ 
        """
        lats, longs = zip(
            *[(39.766706+self.i, 30.525631+self.i), (39.616830811910624, 30.616830811910624),
              (39.546461511615+self.i, 30.5651151531+self.i)

            
            ])
        """
        """
        self.lats, self.longs = zip(
            *[(x, y), (x+0.1, y),
              (x+0.00054, y+0.15613)

            
            ])
        """  
        
        
        
        #self.gmap = gmplot.GoogleMapPlotter(
         #   self.lats, self.longs, 14, apikey='AIzaSyDpgKJ3LZciHRNcrHQoVdgbWRgim_Y5jU0')
        #self.gmap.enable_marker_dropping(color='orange')
        #self.gmap.marker(39, 30, color='cornflowerblue')
        if self.maxMarker <=15 and self.checklist[0] != self.lats:
        
            self.gmap.marker(self.lats, self.longs, color='cornflowerblue')
            
            #self.gmap.scatter(self.lats, self.longs, marker=True, size= 1000)
            self.gmap.draw('geomap.html')
            self.maxMarker+=1
        
        self.checklist.clear()
        self.checklist.append(self.lats) 
        
        
        
           
class serverUi(QWidget):
    
    def __init__(self):
        super().__init__()

        self.login = LoggedIn()

        self.init_server_ui()
    
    def init_server_ui(self):

        self.received_text = QtWidgets.QTextEdit()
        self.deleteTextButton = QtWidgets.QPushButton("CLEAR")
        self.clientButton = QtWidgets.QPushButton("CLIENT")

        v_box = QtWidgets.QVBoxLayout()
        v_box.addWidget(self.received_text)
        v_box.addWidget(self.deleteTextButton)
        v_box.addWidget(self.clientButton)

        self.deleteTextButton.clicked.connect(self.clickServerUi)
        self.clientButton.clicked.connect(self.clickServerUi)

        #self.received_text.setPlainText(data.decode('utf-8'))
        self.update_serverText(b'Server:')

        self.setLayout(v_box)

    def update_serverText(self,text):
        
        threading.Timer(2, self.update_serverText, args=(text,))
        self.received_text.setPlainText(text.decode('utf-8'))

    def clickServerUi(self):

        senderSrv = self.sender()

        if senderSrv.text() == "CLEAR":
            self.received_text.clear()
        else: 
            widget.addWidget(LoggedIn())
            widget.setCurrentIndex(widget.currentIndex() + 1)


class Map(QWidget):
    
    def __init__(self):
        
        super().__init__()
        self.setWindowTitle('Map')
        self.window_width, self.window_height = 800, 550
        self.setMinimumSize(self.window_width, self.window_height)

        layout = QVBoxLayout()
        self.setLayout(layout)

        #apikey = 'AIzaSyDpgKJ3LZciHRNcrHQoVdgbWRgim_Y5jU0'
        self.draw_marker()
        #gmap = gmplot.GoogleMapPlotter(
            #39.766706, 30.525631, 14, apikey=apikey)

        #gmap.marker(39.766706, 30.525631, color='cornflowerblue')

        #gmap.draw('geomap.html')

        #coordinate = received_coordinates.connectClient("").decode('utf-8')
        #coordinate_list = coordinate.strip(')(').split(', ')
        #cordinateX = float(coordinate_list[0])
        #cordinateY = float(coordinate_list[1])
        
        #print(cordinateX, cordinateY)
        """
        m = folium.Map(
            tiles='Stamen Terrain',
            zoom_start=13,
            location=(39.766706, 30.525631)
        )
        
        N = 20

        points = np.array([np.random.uniform(low=35, high=60, size=N),
                          np.random.uniform(low=-12, high= 30, size=N)]).T
        
        plugins.MarkerCluster(points).add_to(m)

        # save map data to data object
        data = io.BytesIO()
        m.save(data, close_file=False)
        """
        webView = QWebEngineView()
        webView.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        webView.load(QUrl.fromLocalFile(
            QDir.current().absoluteFilePath('geomap.html')))
        #webView.setHtml(data.getvalue().decode())
        layout.addWidget(webView)

    def draw_marker(self):

        with open('coordinates.json') as file:
            coordinates = json.load(file)
            print(coordinates)


        for values in coordinates['coordinates']:
            coordinateX = values['xValue']
            coordinateY = values['yValue']
            try:
                
                self.gmap.marker(coordinateX, coordinateY, color='cornflowerblue')
                self.gmap.draw('geomap.html')
            
            except:
                print("ZAAAA")
            print(coordinateX,coordinateY)


"""
    def draw_marker(self):    
        while 1:
            with open('coordinates.json') as file:
                coordinates = json.load(file)
                print(coordinates)

                values = coordinates['coordinates']
                print(values)
                coordinateX = values[0]['xValue']
                coordinateY = values[0]['yValue']
                #coordinateX = values['xValue']
                #coordinateY = values['yValue']
                mark = folium.Marker(location=[coordinateX, coordinateY],
                             icon=folium.Icon(color='red', icon='euro', prefix='fa')).add_to(self.m)
                print(coordinateX,coordinateY)
                time.sleep(10)
"""

class Menu(QMainWindow):
    
    def __init__(self):

        super().__init__()

        self.pencere = LoggedIn()

        self.setCentralWidget(self.pencere)

        self.createMenu()
        
    def createMenu(self):
        
        menubar = self.menuBar()

        clientMenu = menubar.addMenu("Client")
        MapMenu = menubar.addMenu("MAP")

        click_client = QAction("Client",self)
        click_map = QAction("Map",self)
        clientMenu.addAction(click_client)
        MapMenu.addAction(click_map)
        clientMenu.triggered.connect(self.runMenus)
        MapMenu.triggered.connect(self.runMenus)

        self.setWindowTitle("GPS App")
        self.show()

    def runMenus(self,action):
        if action.text() == "Client":
            print("Clienta basildi!!!")
        else:
            print("Mapa basildi!!!")

app = QtWidgets.QApplication(sys.argv)

mainWindow = Window()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainWindow)
widget.resize(800,550)

widget.show()

sys.exit(app.exec_())

"""
class Server():
    def connectServer(self):
        host = socket.gethostbyname(socket.gethostname())
        port = 1024
        format = 'utf-8'

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((host, port))

        while True:
            data, addr = sock.recvfrom(2048)
            print(str(data))
            msgServer = "Coming from UDP Server".encode(format)
            sock.sendto(msgServer, addr)


class Client():
    def connectClient(self):
        host = socket.gethostbyname(socket.gethostname())
        port = 1024
        format = 'utf-8'

        client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        msgClient = "Sended from UDP Client"
        client_sock.sendto(msgClient.encode(format), (host, port))
        data, addr = client_sock.recvfrom(2048)
        print("From Server: {}".format(str(data)))
        client_sock.close()
"""



