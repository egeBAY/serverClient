import socket
import random
import threading
import json


class Server():

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = 1024
        self.format = 'utf-8'
        self.sock.bind((self.host, self.port))
        

    def generateCoordinate(self):
       
       with open('coordinates.json', "r") as f:
           data = json.load(f)
       
       generated = random.random()

       generatedX = 39 + generated
       generatedY = 30 + generated

       for item in data['coordinates']:
           item['xValue'] = generatedX
           item['yValue'] = generatedY

       with open('coordinates.json',"w") as f:
            json.dump(data,f, indent=2)
            
       return generatedX,generatedY



    def listenClient(self):
        

        
        tServer = threading.Timer(2,self.listenClient)
        tServer.daemon = True
        tServer.start()
 
        while True: 
            data, addr = self.sock.recvfrom(2048)
            if not data.decode(self.format) == "iptal":
                print(str(data))
            msgServer = str(self.generateCoordinate()).encode(self.format)
            self.sock.sendto(msgServer, addr)


s = Server()
s.listenClient()


"""
    host = socket.gethostbyname(socket.gethostname())
    port = 1024
    format = 'utf-8'

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
"""
"""
data, addr = self.sock.recvfrom(2048)
print(str(data))
msgServer = str(self.generateRandom()).encode(self.format)
self.sock.sendto(msgServer, addr)
"""
    
