import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'src/') ))

import socket
import json
from utils import *

# https://community.appinventor.mit.edu/t/gottext-not-triggered/34897/2
# https://mundoprojetado.com.br/controlando-nodemcu-por-aplicativo-android/
# https://community.appinventor.mit.edu/t/http-post-format-problem/11506/5

# -1 < x,y < 1 -> robo para
#  x > 5 -> robo anda para a direita
#  x < -5 -> robo anda para a esquerda
#  y > 5 -> robo anda para baixo
#  y < -5 -> robo anda para cima

# Conectar no Vrep
clientID = connect_2_sim()
test_connection(clientID)

# Recuperar handlers do dr20
left_motor_handle, right_motor_handle = get_dr20_motor_handles_(clientID)

def move_safe(direction, clientID, left_motor_handle, right_motor_handle):
    if direction == 'f':
        print('Moving forward')
        robot_run(clientID, left_motor_handle, right_motor_handle,1,1)
    if direction == 'b':
        print('Moving backward')
        robot_run(clientID, left_motor_handle, right_motor_handle,-1,-1)
    if direction == 'l':
        print('Moving left')
        robot_run(clientID, left_motor_handle, right_motor_handle,-1,1)
    if direction == 'r':
        print('Moving right')
        robot_run(clientID, left_motor_handle, right_motor_handle,1,-1)
    if direction == 's':
        print("Stopping")
        robot_run(clientID, left_motor_handle, right_motor_handle,0,0)


# ACELERAÇÃO
acceleration_dict = {}

# VARIÁVEIS DO SERVIDOR
HOST = ""  # any connection allowed
PORT = 8000  # Port to listen on (non-privileged ports are > 1023)
confirmation = b"HTTP/1.1 200 OK\n\n" # ackowledge the connection

# CRIANDO SOCKET DE SERVIDOR
serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # criacao do socket TCP
serverSocket.bind((HOST,PORT)) # bind do ip do servidor com a porta
serverSocket.listen(1) # socket pronto para 'ouvir' conexoes

print ('Servidor TCP esperando conexoes na porta %d ...' % (PORT))

# LOOP SERVIDOR-CONTROLE
while 1:
    # CONEXAO CLIENTE
    connectionSocket, addr = serverSocket.accept() # aceita as conexoes dos clientes
    sentence = connectionSocket.recv(16384) # recebe dados do cliente
    sentence_decoded = sentence.decode('utf-8')
    connectionSocket.send(confirmation); # confirmação de recebimento
    connectionSocket.close() # encerra o socket com o cliente

    # SEPARANDO A MENSAGEM
    chunks = sentence_decoded.split('\n')
    msg = chunks[-1]

    # PROCESSANDO A MENSAGEM
    if len(msg)>10:
        # GERANDO DICIONÁRIO COM VALORES DE ACELERAÇÃO
        dict_json = json.loads(msg)
        for key, value in zip(dict_json.keys(), dict_json.values()):
            acceleration_dict[key] = float(value)
        # print(acceleration_dict)


    # MOVENDO O ROBO
    if acceleration_dict['x']<-5:
        move_safe('r', clientID, left_motor_handle, right_motor_handle)
    elif acceleration_dict['x']>5:
        move_safe('l', clientID, left_motor_handle, right_motor_handle)
    elif acceleration_dict['y']>5:
        move_safe('b', clientID, left_motor_handle, right_motor_handle)
    elif acceleration_dict['y']<-5:
        move_safe('f', clientID, left_motor_handle, right_motor_handle)
    else:
        move_safe('s', clientID, left_motor_handle, right_motor_handle)
serverSocket.close() # encerra o socket do servidor
