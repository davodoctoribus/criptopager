import socket
import json
import threading
import time

#Especificação do endereço IP e porta da rede de computadores
HOST = '' #escutando todas as redes
PORT = 5060

#Criação do socket por TCP
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#Relaciona o socket criado ao IP e à Porta configurados e coloca um limite no número de conexões
servidor.bind((HOST, PORT))
servidor.listen(5)

conexoes = []       # lista com todos os pagers atualmente conectados
lock = threading.Lock()  # evita que duas threads mexam na lista ao mesmo tempo

def aceitar_conexoes(): #não trava o envio de mensagens, aceita novos receptores (pagers) a qualquer momento.
    while True:
        conexao, endereco = servidor.accept()
        with lock:
            conexoes.append(conexao)
        print(f"[+] Novo pager conectado: {endereco}")

import socket
import json
import threading
import time

# Especificação do endereço IP e porta da rede de computadores
HOST = ''
PORT = 5050  # portas 0-1023 são reservadas pelo sistema, por isso trocamos a porta 1

# Criação do socket por TCP
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Relaciona o socket criado ao IP e à Porta configurados
servidor.bind((HOST, PORT))
servidor.listen(5)  # permite várias conexões pendentes na fila (vários pagers)

conexoes = []       # lista com todos os pagers atualmente conectados
lock = threading.Lock()  # evita que duas threads mexam na lista ao mesmo tempo


def aceitar_conexoes():
    """Roda em background aceitando novos pagers a qualquer momento,
    sem travar o envio de mensagens."""
    while True:
        conexao, endereco = servidor.accept()
        with lock:
            conexoes.append(conexao)
        print(f"[+] Novo pager conectado: {endereco}")


def enviar_mensagem(capcode, mensagem):
    #Mudei a lógica porque o pager transmite a mensagem para TODOS os pagers conectados.
    #Assim reproduz o comportamento real: a central emite para todos,
    #e cada pager decide se a mensagem é para ele (nosso caso é comparando o capcode).
    #É justamente esse broadcast sem criptografia que torna o sistema facilmente interceptável.
    payload = {'capcode': capcode, 'mensagem': mensagem, 'tempo': time.time()}
    dados = json.dumps(payload).encode()  # dicionário -> string JSON -> bytes

    with lock:
        desconectados = []
        for conexao in conexoes:
            try:
                conexao.sendall(dados)
            except (BrokenPipeError, ConnectionResetError):
                desconectados.append(conexao)  # pager caiu, marcar para remoção
        for conexao in desconectados:
            conexoes.remove(conexao)


if __name__ == "__main__":
    # Thread separado para aceitar conexões em segundo plano, sem bloquear o envio de mensagens
    threading.Thread(target=aceitar_conexoes, daemon=True).start()
    print(f"Central (transmissor) ativa na porta {PORT}. Aguardando pagers...")

    while True:
        capcode = input("\nCapcode do destinatário: ")
        mensagem = input("Mensagem: ")
        enviar_mensagem(capcode, mensagem)
        print("Mensagem transmitida para todos os pagers conectados.")