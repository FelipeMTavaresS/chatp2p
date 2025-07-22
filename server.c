#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <pthread.h>

#define PORT 8888
#define BUFFER_SIZE 1024

int client_socket;

void *receber(void *arg) {
    char buffer[BUFFER_SIZE];
    while (1) {
        memset(buffer, 0, BUFFER_SIZE);
        int len = recv(client_socket, buffer, BUFFER_SIZE, 0);
        if (len <= 0) break;
        printf("\nCliente: %s", buffer);
        printf("Você: "); fflush(stdout);
    }
    return NULL;
}

void *enviar(void *arg) {
    char buffer[BUFFER_SIZE];
    while (1) {
        printf("Você: ");
        fgets(buffer, BUFFER_SIZE, stdin);
        send(client_socket, buffer, strlen(buffer), 0);
    }
    return NULL;
}

int main() {
    int server_socket;
    struct sockaddr_in server_addr, client_addr;
    socklen_t client_len = sizeof(client_addr);

    // Criar socket
    server_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (server_socket < 0) {
        perror("Erro ao criar socket");
        exit(1);
    }

    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(PORT);

    // Bind e listen
    bind(server_socket, (struct sockaddr *)&server_addr, sizeof(server_addr));
    listen(server_socket, 1);
    printf("Aguardando conexão...\n");

    client_socket = accept(server_socket, (struct sockaddr *)&client_addr, &client_len);
    printf("Cliente conectado!\n");

    pthread_t th1, th2;
    pthread_create(&th1, NULL, receber, NULL);
    pthread_create(&th2, NULL, enviar, NULL);

    pthread_join(th1, NULL);
    pthread_join(th2, NULL);

    close(client_socket);
    close(server_socket);
    return 0;
}
