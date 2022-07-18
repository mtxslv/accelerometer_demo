import socket
import json

# https://community.appinventor.mit.edu/t/gottext-not-triggered/34897/2
# https://mundoprojetado.com.br/controlando-nodemcu-por-aplicativo-android/
# https://community.appinventor.mit.edu/t/http-post-format-problem/11506/5

# -1 < x,y < 1 -> robo para
#  x > 5 -> robo anda para a direita
#  x < -5 -> robo anda para a esquerda
#  y > 5 -> robo anda para baixo
#  y < -5 -> robo anda para cima

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
    
    # SEPARANDO A MENSAGEM
    chunks = sentence_decoded.split('\n')
    msg = chunks[-1]

    # PROCESSANDO A MENSAGEM
    if len(msg)<10:
        print(f' STOP ROBOT')
    else:
        # GERANDO DICIONÁRIO COM VALORES DE ACELERAÇÃO
        dict_json = json.loads(msg)
        for key, value in zip(dict_json.keys(), dict_json.values()):
            acceleration_dict[key] = float(value)
        print(acceleration_dict)
    connectionSocket.close() # encerra o socket com o cliente
serverSocket.close() # encerra o socket do servidor
