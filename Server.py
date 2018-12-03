import socket
s = socket.socket()
print("Socket successfully created!")

port = 12345

s.bind(('', port))
print("Socket binded to %s" %(port))
s.listen(5)
print("Socket is listening!")

#Block for Data Collection from file
f = open("input.txt", "r")
flines = f.readlines()
itemData = {}
for i in range(1,len(flines)):
    nline = flines[i].split()
    itemData[nline[0]] = [int(nline[1]), int(nline[2])] #Puts data in dictionary organized by {"Item Name":[Units,Price]} for updating and reading
print(itemData)
f.close()

#Transmitting Block
while True:
    c, addr = s.accept()
    print("Got connection from", addr)
    c.send(str.encode('Thank you for connecting!'))
    s.listen(5)
    print("It looks like were receiving a message, It says: ")
    print((c.recv(1024)).decode('utf-8'))
    c.close()
