import socket
import threading

# Define o endereço IP do servidor e a porta que será usada
HOST = '127.0.0.1' # endereço IP local
PORT = 5000

# Cria um objeto de socket e configura para receber conexões
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

# Cria um dicionário para armazenar os clientes conectados
clientes = {}

# Função para enviar uma mensagem para todos os clientes, exceto o cliente que enviou a mensagem
def broadcast(mensagem, cliente_origem):
    for cliente in clientes:
        if cliente != cliente_origem:
            cliente.send(mensagem)

# Função que será executada em uma thread para lidar com um cliente
def handle_cliente(cliente):
    # Envia uma mensagem de boas-vindas para o cliente
    cliente.send('Bem-vindo ao chat!\n'.encode('utf-8'))
    while True:
        try:
            # Recebe a mensagem do cliente
            mensagem = cliente.recv(1024)
            # Se a mensagem estiver vazia, o cliente foi desconectado
            if not mensagem:
                del clientes[cliente]
                cliente.close()
                broadcast(f'Cliente {clientes[cliente]} desconectou.\n'.encode('utf-8'), None)
                break
            # Se a mensagem não estiver vazia, envia a mensagem para todos os clientes, exceto o cliente que enviou a mensagem
            broadcast(mensagem, cliente)
        except:
            # Se ocorrer algum erro, remove o cliente da lista e fecha a conexão
            del clientes[cliente]
            cliente.close()
            broadcast(f'Cliente {clientes[cliente]} desconectou.\n'.encode('utf-8'), None)
            break

# Função principal que lida com a conexão dos clientes
def main():
    while True:
        # Aceita uma conexão de um novo cliente
        cliente, endereco = server_socket.accept()
        # Adiciona o cliente ao dicionário de clientes conectados, com um ID único
        clientes[cliente] = len(clientes) + 1
        # Imprime uma mensagem indicando a conexão do cliente
        print(f'Conexão recebida de {endereco[0]}:{endereco[1]}')
        # Cria uma thread para lidar com o cliente
        thread = threading.Thread(target=handle_cliente, args=(cliente,))
        thread.start()


main()
