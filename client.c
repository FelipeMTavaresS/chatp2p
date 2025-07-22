#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <pthread.h>

#define PORT 8888
#define BUFFER_SIZE 1024

int sock;

void *receber(void *arg) {
    char buffer[BUFFER_SIZE];
    while (1) {
        memset(buffer, 0, BUFFER_SIZE);
        int len = recv(sock, buffer, BUFFER_SIZE, 0);
        if (len <= 0) break;
        printf("\nServidor: %s", buffer);
        printf("Você: "); fflush(stdout);
    }
    return NULL;
}

void *enviar(void *arg) {
    char buffer[BUFFER_SIZE];
    while (1) {
        printf("Você: ");
        fgets(buffer, BUFFER_SIZE, stdin);
        send(sock, buffer, strlen(buffer), 0);
    }
    return NULL;
}

int main() {
    struct sockaddr_in server_addr;

    // Criar socket
    sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) {
        perror("Erro ao criar socket");
        exit(1);
    }

    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(PORT);
    server_addr.sin_addr.s_addr = inet_addr("127.0.0.1"); // Altere para IP do servidor se necessário

    // Conectar ao servidor
    if (connect(sock, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        perror("Erro ao conectar");
        exit(1);
    }

    printf("Conectado ao servidor!\n");

    pthread_t th1, th2;
    pthread_create(&th1, NULL, receber, NULL);
    pthread_create(&th2, NULL, enviar, NULL);

    pthread_join(th1, NULL);
    pthread_join(th2, NULL);

    close(sock);
    return 0;
}
