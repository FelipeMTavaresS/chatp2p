import socket
import threading
import base64

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

# Chave simples para codificação (não é criptografia real!)
ENCODING_KEY = "ChatP2P2025"

def encode_message(message):
    """Codifica uma mensagem usando base64"""
    encoded = base64.b64encode(message.encode('utf-8')).decode('utf-8')
    return encoded

def decode_message(encoded_message):
    """Decodifica uma mensagem base64"""
    try:
        decoded = base64.b64decode(encoded_message.encode('utf-8')).decode('utf-8')
        return decoded
    except:
        return "[ERRO: Mensagem não pôde ser decodificada]"

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                # Codifica a mensagem antes de enviar
                encoded_msg = encode_message(message)
                client.send(encoded_msg.encode('utf-8'))
            except:
                clients.remove(client)

def handle_client(client_socket, address):
    print(f"[+] Nova conexão de {address}")
    
    # Envia sinal de que o servidor suporta codificação
    client_socket.send("ENCODING:ENABLED".encode('utf-8'))
    
    while True:
        try:
            msg = client_socket.recv(1024).decode('utf-8')
            if not msg:
                break
            
            # Decodifica a mensagem recebida
            decoded_msg = decode_message(msg)
            print(f"[DEBUG] Mensagem recebida de {address}: {decoded_msg}")
            
            # Retransmite a mensagem decodificada
            broadcast(decoded_msg, client_socket)
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
    print("[*] Servidor de chat com codificação escutando em 0.0.0.0:5555...")
    print(f"[*] Para conectar de outros computadores, use o IP: {local_ip}")
    print(f"[*] Comando para outros PCs: py client_simple.py (e digite {local_ip})")
    print("[*] Codificação: Base64 (demonstração)")
    print("-" * 50)

    while True:
        client_socket, addr = server.accept()
        clients.append(client_socket)
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()

if __name__ == "__main__":
    main()
