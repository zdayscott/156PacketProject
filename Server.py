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
notifD = "Default"

##FUNCTIONS##
def getSocket(addr):
    global clients
    for i in range (0, len(clients)-1):
        if (clients[i][1]== addr):
            c = clients[i][0]
            return c

def itemWon(itemName, addr):
    win = "Server: Congratulations! You've won 1 " + itemName + ". "
    c = None
    global winnerInfo
    global itemData
    for i in range(0,len(clients)-1):
        if (client[i][1]==addr):
            c = client[i][0]
    c.send(("Won").encode('utf-8'))
    c.send(win.encode('utf-8'))
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
    print("solicitbids started")
    invite = "Server: You may now bid on an item. "
    global bidTracker
    global clients
    for i in range (0,len(clients) - 1):
        c = clients[i][0]
        c.send(invite.encode('utf-8'))
        temp = (c.recv(1024)).decode('utf-8', 'ignore') #Will Recv string Item Name and added into bids array
        print(clients[i][1])
        print(temp)
        bidTracker[addr] = temp

#Checks for case where one item was bid on by more than 1 client, returns dict of items: [addr]
def checkMultBid():
    print("multibids started")
    global multiBid
    global bidTracker
    for key in bidTracker:
        copy = bidTracker.copy()
        tempTup = bidTracker[key]
        del copy[key]
        for k in copy:
            if (bidTracker[key][0] == copy[k][0]):
                itemName = bidTracker[key][0]
                appendValue(multiBid, itemName, key) #puts item&addr into conflicting bid dict


def bidWarMode(itemName, listAddr):
    msg1="Server: Other clients have bid on " + itemName + "."
    itemWon(itemName, bidWarH(itemName, listAddr, 50, None))


#recursive call that keeps bid war going, returns addr of person who won
def bidWarH(itemName, listAddr, price, leader):
    global clients
    newPrice = price+1
    notifW = "Winning"
    notifO = "Outbid"
    losing = "Server: You have been outbid by another client, submit a new bid or lose the item. The price to beat is: $" + str(price+1) + ". "
    winning = "Server: You are currently winning the bid with a price of $" + str(newPrice) + ". "
    lost = "Server: I'm sorry but you did not win " + itemName + ". "
    if (newPrice >= itemData[itemName][1]):
        if clients[i][0] in listAddr:
                clients[i][0].send(lost.encode('utf-8'))
        return leader
    nleader = listAddr[random.randint(0,len(listAddr)-1)]
    listAddr.remove(nleader)
    if (leader != None):
        listAddr.append(leader)
    newBids = []
    for i in range(0, len(clients)-1):
        if (clients[i][1] == nleader):
            clients[i][0].send(notifW.encode('utf-8'))
            clients[i][0].send(winning.encode('utf-8'))
        elif clients[i][0] in listAddr:
                clients[i][0].send(notifO.encode('utf-8'))
                clients[i][0].send(losing.encode('utf-8'))
                clients[i][0].send(pickle.dumps(newPrice))
                clients[i][0].settimeout(5.0)
                if (pickle.loads(clients[i][0].rcv(1024)) == newPrice+1):
                    newBids.append(clients[i][1])
    if (newBids!= []):
        bidWarH(itemName, newBids, newPrice, nleader)
    return nleader



s = socket.socket()
port = 12345
s.bind(('', port))
print("Listening for Clients")
s.listen(5)

#intializes array of clients
for i in range(0,2):
    c, addr = s.accept()
    clients.append((c,addr))
    print('Connected to ', addr)

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
    for i in range(0,len(clients)):
        c = clients[i][0]
        print('sending itemdata to ')
        print(clients[i][1])
        c.send(pickle.dumps(itemData))
    solicitBids()
    checkMultBid()
    for key in bidTracker:
        for k in multiBid:
            if key not in multiBid[k]:
                z = getSocket(key)
                z.send(notifD.encode('utf-8'))
                z.send(("Server: No one else has bid on your item.").encode('utf-8'))
                itemWon(bidTacker[key],key)
    for key in multiBid:
        bidWarMode(key, multiBid[key])
    multiBid.clear()
    bidTracker.clear()
