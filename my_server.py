import socket

# https://community.appinventor.mit.edu/t/gottext-not-triggered/34897/2
# https://mundoprojetado.com.br/controlando-nodemcu-por-aplicativo-android/
# https://community.appinventor.mit.edu/t/http-post-format-problem/11506/5


HOST = ""  # any connection allowed
PORT = 8000  # Port to listen on (non-privileged ports are > 1023)
confirmation = b"HTTP/1.1 200 OK\n\n"

serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # criacao do socket TCP
serverSocket.bind((HOST,PORT)) # bind do ip do servidor com a porta
serverSocket.listen(1) # socket pronto para 'ouvir' conexoes
print ('Servidor TCP esperando conexoes na porta %d ...' % (PORT))
while 1:
    connectionSocket, addr = serverSocket.accept() # aceita as conexoes dos clientes
    sentence = connectionSocket.recv(16384) # recebe dados do cliente
    sentence = sentence.decode('utf-8')
    print(f'{sentence} | {type(sentence)}')
    connectionSocket.send(confirmation) # confirmação de recebimento
    connectionSocket.close() # encerra o socket com o cliente
serverSocket.close() # encerra o socket do servidor
