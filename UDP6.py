# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UDP6.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt,QTimer, pyqtSignal
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QAction, QLabel,QMainWindow,QWidget
from PyQt5.QtGui import QPixmap, QMovie
import sys
import socket
import threading

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(687, 514)
        self.gridLayout_2 = QtWidgets.QGridLayout(Form)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.stackedWidget = QtWidgets.QStackedWidget(Form)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.gridLayout = QtWidgets.QGridLayout(self.page)
        self.gridLayout.setObjectName("gridLayout")
        self.sendingText = QtWidgets.QTextEdit(self.page)
        self.sendingText.setObjectName("sendingText")
        self.gridLayout.addWidget(self.sendingText, 0, 0, 1, 1)
        self.sendButton = QtWidgets.QPushButton(self.page)
        self.sendButton.setObjectName("sendButton")
        self.gridLayout.addWidget(self.sendButton, 1, 0, 1, 1)
        self.deleteButton = QtWidgets.QPushButton(self.page)
        self.deleteButton.setObjectName("deleteButton")
        self.gridLayout.addWidget(self.deleteButton, 2, 0, 1, 1)
        self.serverButton = QtWidgets.QPushButton(self.page)
        self.serverButton.setObjectName("serverButton")
        self.gridLayout.addWidget(self.serverButton, 3, 0, 1, 1)
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.page_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.received_text = QtWidgets.QLabel(self.page_2)
        self.received_text.setText("")
        self.received_text.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.received_text.setObjectName("received_text")
        self.gridLayout_3.addWidget(self.received_text, 0, 0, 1, 1)
        self.deleteTextButton = QtWidgets.QPushButton(self.page_2)
        self.deleteTextButton.setObjectName("deleteTextButton")
        self.gridLayout_3.addWidget(self.deleteTextButton, 1, 0, 1, 1)
        self.clientButton = QtWidgets.QPushButton(self.page_2)
        self.clientButton.setObjectName("clientButton")
        self.gridLayout_3.addWidget(self.clientButton, 2, 0, 1, 1)
        self.stackedWidget.addWidget(self.page_2)
        self.gridLayout_2.addWidget(self.stackedWidget, 0, 0, 1, 1)

        self.retranslateUi(Form)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)
        
        self.flag = 0
        self.text = ""
        
        
        #self.connectClient("iptal")
        self.client=LoggedIn()
        self.sendButton.clicked.connect(self.send)
        
    
        
    def send(self):
        print("Server'a {} gönderildi.".format(self.sendingText.toPlainText()))
        self.client.connectClient_2(self.sendingText.toPlainText())
        self.flag = 1

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "UDP"))
        self.sendButton.setText(_translate("Form", "GONDER"))
        self.deleteButton.setText(_translate("Form", "TEMIZLE"))
        self.serverButton.setText(_translate("Form", "SERVER"))
        self.deleteTextButton.setText(_translate("Form", "CLEAR"))
        self.clientButton.setText(_translate("Form", "CLIENT"))
        
class LoggedIn(QWidget):
    progress = pyqtSignal(str)
    def __init__(self):

        super().__init__()
        
        
        
        
        
        self.text=""
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
            t1.daemon=True
            t1.start()
            
            client_sock.sendto(msg.encode(format), (host, port))
            
            
            data, addr = client_sock.recvfrom(2048)
            #msg=str(data)
            print("From Server1: {}".format(str(data)))
            
            #self.sendingText.setPlainText(msg)
            self.text=str(data)+"\n"+self.text
            self.progress.emit(self.text)
            self.progress.connect(self.sendingText)
            #if serverUi().flag2 == 1:
             #   print("")
                #serverUi().update_serverText(str(data))
            #serverUi().progress.connect(serverUi().update_serverText)
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
            self.flag2 = 1 

class mywindow(QtWidgets.QWidget):
    
    def __init__(self):
        super(mywindow,self).__init__()
        self.ui=Ui_Form()
        self.ui.setupUi(self)
        
app = QtWidgets.QApplication([])

application = mywindow()

application.show()

sys.exit(app.exec())