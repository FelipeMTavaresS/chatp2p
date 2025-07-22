import socket
import threading
import sys
import base64

# Variável global para codificação
encoding_enabled = False

def encode_message(message):
    """Codifica uma mensagem usando base64"""
    return base64.b64encode(message.encode('utf-8')).decode('utf-8')

def decode_message(encoded_message):
    """Decodifica uma mensagem base64"""
    try:
        return base64.b64decode(encoded_message.encode('utf-8')).decode('utf-8')
    except:
        return "[ERRO: Mensagem não pôde ser decodificada]"

def receive_messages(sock):
    global encoding_enabled
    first_message = True
    
    while True:
        try:
            msg = sock.recv(1024).decode('utf-8')
            
            if first_message:
                # Primeira mensagem verifica se o servidor suporta codificação
                if msg == "ENCODING:ENABLED":
                    encoding_enabled = True
                    print("🔐 Codificação Base64 ativada!")
                    first_message = False
                    continue
            
            if encoding_enabled:
                # Decodifica a mensagem
                decoded_msg = decode_message(msg)
                print(decoded_msg)
            else:
                # Fallback se não tiver codificação
                print(msg)
                
        except Exception as e:
            print(f"[-] Conexão encerrada pelo servidor. {e}")
            break

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    print("=== CLIENTE CHAT COM CODIFICAÇÃO ===")
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
    
    # Aguarda um pouco para receber confirmação de codificação
    import time
    time.sleep(0.5)
    
    if encoding_enabled:
        client.send(encode_message(entry_msg).encode('utf-8'))
    else:
        client.send(entry_msg.encode('utf-8'))

    thread = threading.Thread(target=receive_messages, args=(client,))
    thread.start()

    while True:
        msg = input()
        if msg.lower() == "/sair":
            exit_msg = f"{name} saiu do chat."
            if encoding_enabled:
                client.send(encode_message(exit_msg).encode('utf-8'))
            else:
                client.send(exit_msg.encode('utf-8'))
            client.close()
            break
        print("\033[A\033[K", end="")
        formatted_msg = f"{name}: {msg}"
        print(formatted_msg)
        
        # Envia mensagem codificada
        if encoding_enabled:
            client.send(encode_message(formatted_msg).encode('utf-8'))
        else:
            client.send(formatted_msg.encode('utf-8'))

if __name__ == "__main__":
    main()
