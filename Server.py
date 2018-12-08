import socket
import pickle
import random
'''
TO DO:
- fix an syntax errors
-organize code
- get clients and server to connect

'''

bidTracker = {} #Dictionary to keep track of the bidding process Stored in {addr: Item Name} Format
clients = [] #Array to keep track of client information (socket obj, addr)
multiBid = {} #Dictionary that keeps track of items that are being bid on by multiple clinets {Item Name: [addr]}
itemData = {} #Stores item information taken from input file {ItemName: (units, max bid)}
winnerInfo = {} #stores record of items won {addr: [(itemName, amount owned)]}

##FUNCTIONS##
def getSocket(addr):
    global clients
    for i in range (0,4):
        if (clients[i][1]== addr):
            return clients[i][0]

def itemWon(itemName, addr):
    win = "Server: Congratulations! You've won 1 " + itemName + ". "
    c = None
    global winnerInfo
    global itemData
    for i in range(0,4):
        if (client[i][1]==addr):
            c = client[i][0]
    c.send(str.encode("Won"))
    c.send(str.encode(win))
    if addr not in winnerInfo:
        winnerInfo[addr] = [(itemName, 1)]
    if addr in winnerInfor:
        list = winnerInfo[addr]
        for i in range(len(list)):
            if itemName in list[i]:
                list[i][1]+=1
        list.append((itemName, 1))
    itemData[itemName][0] -= 1

def appendValue(dict, key, val):
    if key in dict:
        list= dict[key]
        if val not in list:
            dict[key].append(val)
    dict[key]= [val]

#Asks array of clients for their bids
def solicitBids():
    invite = "Server: You may now bid on an item. "
    global bidTracker
    global clients
    for i in range (0,len(clients) - 1):
        c = clients[i][0]
        c.send(str.encode(invite))
        temp = c.recv(recv(1024)).decode('utf-8') #Will Recv string Item Name and added into bids array
        bidTracker[addr] = temp

#Checks for case where one item was bid on by more than 1 client, returns dict of items: [addr]
def checkMultBid():
    global multiBid
    global bidTracker
    for key in bidTracker:
        copy = bidTracker
        tempTup = bidTracker[key]
        del dictCopy[key]
        for k in dictCopy:
            if (dict[key][0] == dictCopy[k][0]):
                itemName = dict[key][0]
                appendValue(multiBid, itemName, key) #puts item&addr into conflicting bid dict


def bidWarMode(itemName, listAddr):
    msg1="Server: Other clients have bid on " + itemName + "."
    itemWon(itemName, bidWarH(itemName, listAddr, 50, None))


#recursive call that keeps bid war going, returns addr of person who won
def bidWarH(itemName, listAddr, price, leader):
    global clients
    newPrice = price+1
    losing = "Server: You have been outbid by another client, submit a new bid or lose the item. The price to beat is: $" + str(price+1) + ". "
    winning = "Server: You are currently winning the bid with a price of $" + str(newPrice) + ". "
    lost = "Server: I'm sorry but you did not win " + itemName + ". "
    if (newPrice >= itemData[itemName][1]):
        if clients[i][0] in listAddr:
                clients[i][0].send(str.encode(lost))
        return leader
    nleader = listAddr[random.randint(0,len(listAddr)-1)]
    listAddr.remove(nleader)
    if (leader != None):
        listAddr.append(leader)
    newBids = []
    for i in range(0, len(clients)-1):
        if (clients[i][1] == nleader):
            clients[i][0].send(str.encode("Winning"))
            clients[i][0].send(str.encode(winning))
        elif clients[i][0] in listAddr:
                clients[i][0].send(str.encode("Outbid"))
                clients[i][0].send(str.encode(losing))
                clients[i][0].send(pickle.dumps(newPrice))
                clients[i][0].settimeout(5.0)
                if (pickle.loads(clients[i][0].rcv(1024)) == newPrice+1):
                    newBids.append(clients[i][1])
    if (newBids!= []):
        bidWarH(itemName, newBids, newPrice, nleader)
    return nleader



s = socket.socket()
port = 12345
s.bind(('127.0.0.1', port))
print("Listening for Clients")
s.listen(5)

#intializes array of clients
for i in range(0,4):
    c, addr = s.accept()
    clients[i] = (c,addr)

#Block for Data Collection from file
f = open("input.txt", "r")
flines = f.readlines()
for i in range(1,len(flines)):
    nline = flines[i].split()
    itemData[nline[0]] = [int(nline[1]), int(nline[2])] #Puts data in dictionary organized by {"Item Name":[Units,Price]} for updating and reading
print(itemData)
f.close()

#loop until input, once ended transmit all items in winnerInfo
while True:
    c.send(pickle.dumps(itemData))
    solicitBids()
    checkMultBid()
    for key in bidTracker:
        if key not in multibid:
            c = getSocket(key)
            c.send(str.encode("Default"))
            c.send(str.encode("Server: No one else has bid on your item."))
            itemWon(bidTacker[key],key)
    for key in multiBid:
        bidWarMode(key, multiBid[key])
    multiBid.clear()
    bidTracker.clear()
