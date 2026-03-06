import socket
from threading import Thread
import random
clients_list = {}

class GroupChat:
    
    def __init__(self,host='0.0.0.0',port=5656):
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.host = host 
        self.port = port 
        
    def clients(self,conn,addr):
        
        with conn: 
            while True:
                try:
                    data = conn.recv(1024)
                    if not data:
                        break 
                    self.broadcast(data,conn)
                except Exception as e:
                    print(f'Error Client Connection {addr[0]} : Error {e}\r\n')
                    break 
        self.broadcast(f'[server] Client Disconnect {addr[0]}\r\n'.encode(),conn)
        del clients_list[conn]
    
    def broadcast(self,data,sender):
        msg = data.decode()
        for conn in clients_list:
            if conn!=sender:
                try: 
                    conn.sendall(msg.encode())
                except:
                    del clients_list[conn]
            
                
    def setConf(self):
        self.socket.bind((self.host,self.port))
        self.socket.listen()
    

    def getConn(self):
        self.setConf()
        while True:
            conn , addr = self.socket.accept()
            t = Thread(target=self.clients,args=(conn,addr))
            t.start()
        
GroupChat().getConn()
    