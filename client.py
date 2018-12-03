import socket
import sys
import random

#Function that returns a Bool to determine whether to bid on item or not
def probBid():
    chance = random.randint(0,100)
    return(chance >= 0 and chance <= 33)

s = socket.socket()

port = 12345

s.connect(('127.0.0.1', port))

print((s.recv(1024)).decode('utf-8'))
s.send(str.encode('Hope all is well!'))

s.close()
