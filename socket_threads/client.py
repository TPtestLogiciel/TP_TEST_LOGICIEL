import socket
import threading
import sys

class message_e(threading.Thread):
    '''class qui gere les messages envoyés'''
    def __init__(self):
        threading.Thread.__init__(self)
        self.e = ''
     
    def run(self):
        while(True):
            self.e = input('>>>: ')
            c.send(self.e.encode())
            # print('client: '+ self.e)
            if(self.e == 'close'):
                sys.exit()
                
class message_r(threading.Thread):
    '''class qui gere les messages reçus'''
    def __init__(self):
        threading.Thread.__init__(self)
        self.r = ''
        
    def run(self):
        while(True):
            self.r = c.recv(1024)
            print('<<<: '+ self.r.decode())
   
addr = ('localhost',4400)         
c = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

if(__name__ =='__main__'):
    c.connect(addr)
    envois = message_e()
    recu = message_r()
    envois.start()
    recu.start()