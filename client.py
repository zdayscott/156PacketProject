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
    listKeys = list(dict.keys())
    return listKeys[random.randint(0,9)] #returns random item name to be bid on

s = socket.socket()
port = 12345
s.connect(('10.0.0.97', port))
print('Connected to Server')

while True:
    itemData = pickle.loads(s.recv(4096))
    itemName = chooseItem(itemData)
    print((s.recv(1024)).decode('utf-8', 'ignore'))
    print(willBid + itemName+ ". ")
    s.send(itemName.encode('utf-8'))
    l = True
    while (l):
        choice =(s.recv(1024)).decode('utf-8', 'ignore')
        if (choice == "Outbid"):
            print((s.recv(1024)).decode('utf-8', 'ignore'))
            newPrice = pickle.loads(s.recv(1024)) + 1
            if (probBid()):
                s.send(pickle.dumps(newPrice))
            if (not probBid()):
                    l = False
        elif(choice == "Winning"):
            print((s.recv(1024)).decode('utf-8', 'ignore'))
        elif(choice == "Won"):
            print((s.recv(1024)).decode('utf-8', 'ignore'))
            l = False
        elif(choice == "Default"):
            print((s.recv(1024)).decode('utf-8', 'ignore'))
        else: l = False
        
s.close()
