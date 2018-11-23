import socket
s = socket.socket()
print("Socket successfully created!")

port = 12345

s.bind(('', port))
print("Socket binded to %s" %(port))

s.listen(5)
print("Socket is listening!")

while True:
    c, addr = s.accept()
    print("Got connection from", addr)
    c.send(str.encode('Thank you for connecting!'))
    c.close()