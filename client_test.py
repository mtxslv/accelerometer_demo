# Echo client program
import socket


HOST = '192.168.1.6'    # The remote host
PORT = 8000              # The same port as used by the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    for it in range(0,2):
        msg = b'Hello, world!'
        s.send(msg)
        #s.sendall(b'Hello, world')
        data = s.recv(1024)
        print('Received', repr(data))