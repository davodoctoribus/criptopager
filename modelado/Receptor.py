import socket
import json

# Especificação do receptor
capcode = input("Capcode deste pager (ex: 001): ")
endereco_IP = '127.0.0.1'  # (IP da central) trocar se for outra máquina/rede pelo IP real
PORT = 5056                # necessário ser a mesma porta do transmissor

# Criação do socket e conexão com a central
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.connect((endereco_IP, PORT))
print(f"Pager '{capcode}' conectado à central. Aguardando mensagens...")

while True:  # Manter o pager ativo
    dado = servidor.recv(1024)  # Aguarda o recebimento de dados, limitado a 1024 bytes
    if not dado:  # Caso o transmissor seja desligado, o loop é interrompido
        print("Conexão com a central encerrada.")
        break
    try:
        payload = json.loads(dado.decode())  # Converte os bytes de volta para dicionário
        if payload.get("capcode") == capcode:
            # Mensagem é para este pager: exibir
            print(f"\n[Nova mensagem] {payload['mensagem']}")
        # Se o capcode não bater, a mensagem é recebida mas ignorada,
        # exatamente como um pager real descarta mensagens de outros capcodes
    except (json.JSONDecodeError, KeyError):
        pass  # dado corrompido ou incompleto, ignora e continua esperando

servidor.close()