import socket
import json

#importação da biblioteca Fernet, garante a criptografia 
from cryptography.fernet import Fernet

#Recebe a mesma cave que o transmissor
CHAVE = b'q123456789012345678901234567890123456789012=' # de acorto com o padrão Fernet, tem 32 bytes 
f = Fernet(CHAVE) #inicializa o modo de criptografia

# Especificação do receptor
capcode = input("Capcode deste pager (ex: 001): ")
endereco_IP = '127.0.0.1'  # (IP da central) trocar se for outra máquina/rede pelo IP real
PORT = 5050                # necessário ser a mesma porta do transmissor

# Criação do socket e conexão com a central
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.connect((endereco_IP, PORT))
print(f"Pager '{capcode}' conectado à central. Aguardando mensagens...")

#Tratamento de exceções
while True:  # Manter o pager ativo
    dado = servidor.recv(1024)  # Aguarda o recebimento de dados, limitado a 1024 bytes
    if not dado:  # Caso o transmissor seja desligado, o loop é interrompido
        print("Conexão com a central encerrada.")
        break
    try:
        payload = json.loads(dado.decode())  # Converte os bytes de volta para dicionário
        
        if payload.get("capcode") == capcode:
            msg_cifrada = payload['mensagem'] #conferte da sting encriptada para bytes

            #recebe a msg cifrada, aplica a chave e recupera os bytes originais do texto
            msg_decifrada = f.decrypt(msg_cifrada.encode()).decode() #transfoma os bytes em texto

            # Mensagem é para este pager: exibir
            print(f"\n[Nova mensagem]: {msg_decifrada}")
        # Se o capcode não bater, a mensagem é recebida mas ignorada,
        # exatamente como um pager real descarta mensagens de outros capcodes
    except (json.JSONDecodeError, KeyError):
        pass  # dado corrompido ou incompleto, ignora e continua esperando
    except Exception as e:
        print(f"\n[Erro de Segurança]: Falha ao decifrar a mensagem. Erro: {e}") #evita problemas na criptografia, chaves incorretas, ataques no meio do processo(tentar mudar o texto cifrado enquanto o texto cifrado ta sendo transmitido)
servidor.close()