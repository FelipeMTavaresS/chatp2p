import socket
import threading
from cryptography.fernet import Fernet
import base64

# Chave de criptografia fixa (em produção, use uma chave mais segura)
ENCRYPTION_KEY = Fernet.generate_key()
cipher_suite = Fernet(ENCRYPTION_KEY)

def get_local_ip():
    try:
        # Conecta a um endereço externo para descobrir o IP local
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

clients = []
client_keys = {}  # Armazena as chaves de cada cliente

def send_key_to_client(client_socket):
    """Envia a chave de criptografia para o cliente"""
    key_b64 = base64.b64encode(ENCRYPTION_KEY).decode('utf-8')
    client_socket.send(f"KEY:{key_b64}".encode('utf-8'))

def encrypt_message(message):
    """Criptografa uma mensagem"""
    return cipher_suite.encrypt(message.encode('utf-8'))

def decrypt_message(encrypted_message):
    """Descriptografa uma mensagem"""
    try:
        return cipher_suite.decrypt(encrypted_message).decode('utf-8')
    except:
        return "[ERRO: Mensagem não pôde ser descriptografada]"

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                # Criptografa a mensagem antes de enviar
                encrypted_msg = encrypt_message(message)
                client.send(encrypted_msg)
            except:
                clients.remove(client)

def handle_client(client_socket, address):
    print(f"[+] Nova conexão de {address}")
    
    # Envia a chave de criptografia para o cliente
    send_key_to_client(client_socket)
    
    while True:
        try:
            msg = client_socket.recv(1024)
            if not msg:
                break
            
            # Descriptografa a mensagem recebida
            decrypted_msg = decrypt_message(msg)
            print(f"[DEBUG] Mensagem recebida de {address}: {decrypted_msg}")
            
            # Retransmite a mensagem descriptografada
            broadcast(decrypted_msg, client_socket)
        except Exception as e:
            print(f"[ERRO] Erro ao processar mensagem de {address}: {e}")
            break

    print(f"[-] {address} desconectou.")
    clients.remove(client_socket)
    client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 5555))
    server.listen()

    local_ip = get_local_ip()
    print("[*] Servidor de chat criptografado escutando em 0.0.0.0:5555...")
    print(f"[*] Para conectar de outros computadores, use o IP: {local_ip}")
    print(f"[*] Comando para outros PCs: py client.py (e digite {local_ip})")
    print(f"[*] Chave de criptografia: {base64.b64encode(ENCRYPTION_KEY).decode('utf-8')[:16]}...")
    print("-" * 50)

    while True:
        client_socket, addr = server.accept()
        clients.append(client_socket)
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()

if __name__ == "__main__":
    main()
