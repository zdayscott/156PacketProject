import socket
import sys
import random
import pickle

willBid = "We will bid on "

#Function that returns a Bool to determine whether to bid on item or not
def probBid():
    chance = random.randint(0,100)
    return(chance >= 0 and chance <= 33)
#Accepts a dictionary and randomly selects an item to bid
def chooseItem(dict):
    return dict.keys()[random.randint(0,9)] #returns random item name to be bid on

s = socket.socket()
port = 12345
s.connect(('127.0.0.1', port))

while True:
    itemData = pickle.loads(s.recv(1024))
    itemName = chooseItem(itemData)
    print(s.recv(recv(1024)).decode('utf-8'))
    print(willBid + itemName+ ". ")
    s.send(str.encode(itemName))
    l = True
    while (l):
        choice = (s.recv(1024)).decode('utf-8')
        if (choice == "Outbid"):
            print((s.recv(1024)).decode('utf-8'))
            newPrice = pickle.loads(s.recv(1024)) + 1
            if (probBid()):
                s.send(pickle.dumps(newPrice))
            if (not probBid()):
                    l = False
        elif(choice == "Winning"):
            print((s.recv(1024)).decode('utf-8'))
        elif(choice == "Won"):
            print((s.recv(1024)).decode('utf-8'))
            l = False
        elif(choice == "Default"):
            print((s.recv(1024)).decode('utf-8'))
        else: l = False

s.close()
