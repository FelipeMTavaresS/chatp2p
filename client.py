import socket
import threading
import sys
from cryptography.fernet import Fernet
import base64

# Variáveis globais para criptografia
cipher_suite = None

def setup_encryption(key_b64):
    """Configura a criptografia com a chave recebida do servidor"""
    global cipher_suite
    key = base64.b64decode(key_b64.encode('utf-8'))
    cipher_suite = Fernet(key)

def encrypt_message(message):
    """Criptografa uma mensagem"""
    return cipher_suite.encrypt(message.encode('utf-8'))

def decrypt_message(encrypted_message):
    """Descriptografa uma mensagem"""
    try:
        return cipher_suite.decrypt(encrypted_message).decode('utf-8')
    except:
        return "[ERRO: Mensagem não pôde ser descriptografada]"

def receive_messages(sock):
    global cipher_suite
    first_message = True
    
    while True:
        try:
            msg = sock.recv(1024)
            
            if first_message:
                # Primeira mensagem é a chave de criptografia
                msg_str = msg.decode('utf-8')
                if msg_str.startswith("KEY:"):
                    key_b64 = msg_str[4:]  # Remove "KEY:" do início
                    setup_encryption(key_b64)
                    print("🔐 Criptografia ativada!")
                    first_message = False
                    continue
            
            if cipher_suite:
                # Descriptografa a mensagem
                decrypted_msg = decrypt_message(msg)
                print(decrypted_msg)
            else:
                # Fallback se não tiver criptografia
                print(msg.decode('utf-8'))
                
        except Exception as e:
            print(f"[-] Conexão encerrada pelo servidor. {e}")
            break

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    print("=== CLIENTE CHAT ===")
    print("Opções:")
    print("1. Pressione Enter para conectar ao localhost (mesmo PC)")
    print("2. Digite o IP do servidor para conectar a outro PC na rede")
    
    server_ip = input("\nDigite o IP do servidor (ou Enter para localhost): ").strip()
    
    if not server_ip:
        server_ip = "127.0.0.1"
        print("Conectando ao localhost...")
    else:
        print(f"Conectando ao servidor {server_ip}...")
    
    try:
        client.connect((server_ip, 5555))
        print(f"✓ Conectado ao servidor {server_ip}:5555")
    except:
        print(f"✗ Erro ao conectar com {server_ip}:5555")
        print("Verifique se o servidor está rodando e se o IP está correto.")
        return

    name = input("Digite seu nome: ")
    entry_msg = f"{name} entrou no chat."
    if cipher_suite:
        client.send(encrypt_message(entry_msg))
    else:
        client.send(entry_msg.encode('utf-8'))

    thread = threading.Thread(target=receive_messages, args=(client,))
    thread.start()

    while True:
        msg = input()
        if msg.lower() == "/sair":
            exit_msg = f"{name} saiu do chat."
            if cipher_suite:
                client.send(encrypt_message(exit_msg))
            else:
                client.send(exit_msg.encode('utf-8'))
            client.close()
            break
        print("\033[A\033[K", end="")
        formatted_msg = f"{name}: {msg}"
        print(formatted_msg)
        
        # Envia mensagem criptografada
        if cipher_suite:
            client.send(encrypt_message(formatted_msg))
        else:
            client.send(formatted_msg.encode('utf-8'))

if __name__ == "__main__":
    main()
