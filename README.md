# Chat P2P

Um sistema de chat peer-to-peer simples implementado em C usando sockets TCP e threads.

## Arquivos

- `server.c` - Servidor do chat
- `client.c` - Cliente do chat

## Como compilar

```bash
# Compilar o servidor
gcc -o server server.c -lpthread

# Compilar o cliente
gcc -o client client.c -lpthread
```

## Como executar

1. Execute o servidor primeiro:
```bash
./server
```

2. Em outro terminal, execute o cliente:
```bash
./client
```

## Funcionalidades

- Comunicação em tempo real
- Interface simples de chat
- Suporte a múltiplas conexões (server)
- Threads para envio e recebimento simultâneo

## Requisitos

- GCC
- Bibliotecas pthread
- Sistema operacional Unix/Linux/macOS
