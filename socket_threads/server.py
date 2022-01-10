import socket
import threading
import sys

class message_r(threading.Thread):
    '''class qui gere les messages reçus'''
    def __init__(self):
        threading.Thread.__init__(self)
        self.r = ''
        
    def run(self):
        while(True):
            self.r = conn.recv(1024)
            if(self.r == 'close'):
                sys.exit()
            else:
                print('<<<: '+ self.r.decode())
                
class message_e(threading.Thread):
    '''class qui gere les messages envoyés'''
    def __init__(self):
        threading.Thread.__init__(self)
        self.e = ''
        
    def run(self):
        while(True):
            self.e = input('>>>: ')
            conn.send(self.e.encode())
            # print('serveur: '+ self.e)

addr = ('localhost',4400)

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(addr)
s.listen(5)

if(__name__ == '__main__'):
    print('Waiting for a client to connect')
    conn, addr = s.accept()
    print('client connected')
    recu = message_r()
    envoyer = message_e()
    recu.start()
    envoyer.start()