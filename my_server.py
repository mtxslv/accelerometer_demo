import socket
import json

HOST = ""  # any connection allowed
PORT = 8000  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    print('socket bound')
    print('listening...')
    s.listen()
    while True:
        conn, addr = s.accept()
        with conn:
            raw_data = conn.recv(1024)
            data = raw_data.decode('utf-8')
            print(f'{data} | {type(data)}')
            s.sendto(b'received', addr)

            #json_decoded = json.loads(raw_data)
            #print(json_decoded)
            