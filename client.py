import socket
import threading


g_Name = "unknown"
mutex = threading.Lock()
# Define o endereço IP do servidor e a porta que será usada
HOST = '127.0.0.1' # endereço IP local
PORT = 5000

# Cria um objeto de socket e se conecta ao servidor
cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente_socket.connect((HOST, PORT))

# Função que recebe as mensagens do servidor
def receive():
    while True:
        try:
            # Recebe a mensagem do servidor
            mensagem = cliente_socket.recv(1024).decode('utf-8')
            # Imprime a mensagem
            if (mensagem.startswith("FROM;")):
                split = mensagem.split(";")
                print(split[1] + ": " + split[2])   
            else:
                print(mensagem)
        except:
            # Se ocorrer algum erro, fecha a conexão com o servidor
            cliente_socket.close()
            break

def main():
    # Cria uma thread para receber as mensagens do servidor
    g_Name = input("Digite o seu nome: ")
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()
    while True:
        # Lê uma mensagem do usuário
        mensagem = "FROM;"
        mensagem += g_Name + ";"
        mensagem += input("")
        # Envia a mensagem para o servidor
        cliente_socket.send(mensagem.encode('utf-8'))

main()
