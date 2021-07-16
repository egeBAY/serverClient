import sys
import sqlite3
import socket
import threading
import time

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QAction, QLabel,QMainWindow,QWidget
from PyQt5.QtGui import QPixmap, QMovie
from PyQt5.QtCore import Qt,QTimer


class Window(QtWidgets.QWidget):
    
    def __init__(self):

       super().__init__()
       
       sys.setrecursionlimit(10**6)
       self.baglan()
       self.init_ui() 

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

        self.setFixedSize(128,128)

        self.label_animation = QLabel(self)

        self.movie = QMovie("world.gif")
        self.label_animation.setMovie(self.movie)

        timer = QTimer(self)
        self.movie.start()
        timer.singleShot(8000, self.stopGif)

        self.show()

    def stopGif(self):
        
        self.movie.stop()
        self.close()

class LoggedIn(QWidget):

    def __init__(self):

        super().__init__()
        
        self.flag = 0
        self.init_ui()
        #self.connectServer()
        self.connectClient("iptal")

    def connectServer(self) -> None:
        host = "172.16.60.231"
        #socket.gethostbyname(socket.gethostname())
        port = 1024
        format = 'utf-8'

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((host, port))
        
        while True:
            data, addr = sock.recvfrom(2048)
            print(str(data))
            msgServer = "Coming from UDP Server".encode(format)
            sock.sendto(msgServer, addr)

    def connectClient(self, msg) -> None:
        host = socket.gethostbyname(socket.gethostname())    # "172.16.60.231"
        port = 1024
        format = 'utf-8'
        global data

        if self.flag == 0:
            client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
            t1 = threading.Timer(2,self.connectClient,args=(msg,))
            t1.daemon = True
            t1.start()
           
            client_sock.sendto(msg.encode(format), (host, port))
            
            
            data, addr = client_sock.recvfrom(2048)
            
            print("From Server1: {}".format(str(data)))
            client_sock.close()
            
        self.flag=0

    def connectClient_2(self, msg) -> None:
        #host = "172.16.60.205"
        host = socket.gethostbyname(socket.gethostname())
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

        v_box = QtWidgets.QVBoxLayout()

        v_box.addWidget(self.sendingText)
        v_box.addWidget(self.sendButton)
        v_box.addWidget(self.deleteButton)
        v_box.addWidget(self.serverButton)

        self.deleteButton.clicked.connect(self.click)
        self.sendButton.clicked.connect(self.click)
        self.serverButton.clicked.connect(self.click)

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
        else:
            widget.addWidget(serverUi())
            widget.setCurrentIndex(widget.currentIndex() + 1)

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
        
        self.received_text.setPlainText(text.decode('utf-8'))

    def clickServerUi(self):

        senderSrv = self.sender()

        if senderSrv.text() == "CLEAR":
            self.received_text.clear()
        else: 
            widget.addWidget(LoggedIn())
            widget.setCurrentIndex(widget.currentIndex() + 1)

        

class Menu(QMainWindow):
    
    def __init__(self):

        super().__init__()

        self.pencere = LoggedIn()

        self.setCentralWidget(self.pencere)

        self.createMenu()
        
    def createMenu(self):
        
        menubar = self.menuBar()

        clientMenu = menubar.addMenu("Client")
        serverMenu = menubar.addMenu("Server")

        click_client = QAction("Client",self)
        click_server = QAction("Server",self)
        clientMenu.addAction(click_client)
        serverMenu.addAction(click_server)
        clientMenu.triggered.connect(self.runMenus)
        serverMenu.triggered.connect(self.runMenus)

        self.setWindowTitle("GPS App")
        self.show()

    def runMenus(self,action):
        if action.text() == "Client":
            print("Clienta basildi!!!")
        else:
            print("Servera basildi!!!")

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



