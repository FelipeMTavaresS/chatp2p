# Chat P2P Python

Um sistema de chat peer-to-peer implementado em Python com suporte a criptografia e codificação de mensagens.

## Recursos

- 🔐 **Criptografia/Codificação** - Mensagens protegidas durante transmissão
- 🌐 **Multiplataforma** - Funciona em Windows, Linux e macOS
- 📡 **Rede Local** - Conecte múltiplos computadores na mesma rede
- 💬 **Interface Amigável** - Menu interativo e comandos simples
- ⚡ **Tempo Real** - Comunicação instantânea entre usuários


## Arquivos do Projeto

- `server.py` - Servidor com criptografia AES avançada
- `client.py` - Cliente com criptografia AES avançada  
- `server_simple.py` - Servidor com codificação Base64 (recomendado)
- `client_simple.py` - Cliente com codificação Base64 (recomendado)

## Como usar

### Requisitos
- Python 3.6+
- Biblioteca `cryptography` (para versão com criptografia)

## Exemplo de uso

```bash
# Terminal 1 - Servidor
cd chatp2p
python server_simple.py
# Output: [*] Para conectar de outros computadores, use o IP: 192.168.0.173

# Terminal 2 - Cliente 1
cd chatp2p
python client_simple.py
# Digite o IP: 192.168.0.173 (ou Enter para localhost)
# Digite seu nome: Alice

# Terminal 3 - Cliente 2 (outro computador)
cd chatp2p
python client_simple.py
# Digite o IP: 192.168.0.173
# Digite seu nome: Bob

# Agora Alice e Bob podem conversar!
```

## 🚀 Começar rapidamente

1. **Clone ou baixe o projeto**
2. **Navegue para a pasta:** `cd chatp2p`
3. **Execute o servidor:** `python server_simple.py`
4. **Em outro terminal, execute o cliente:** `python client_simple.py`
5. **Pressione Enter** para conectar ao localhost
6. **Digite seu nome** e comece a conversar!

---

**💡 Dica:** Use a versão `_simple` para garantir que funcione sempre, sem problemas de dependências!

### Opção 1: Versão Simples (Recomendada)
**Usa codificação Base64 - funciona sempre!**

1. **Iniciar o servidor:**
   ```bash
   cd chatp2p
   python server_simple.py
   ```

2. **Conectar clientes:**
   ```bash
   cd chatp2p
   python client_simple.py
   ```

### Opção 2: Versão com Criptografia
**Usa criptografia AES - requer biblioteca adicional**

1. **Instalar dependência:**
   ```bash
   pip install cryptography
   ```

2. **Iniciar o servidor:**
   ```bash
   cd chatp2p
   python server.py
   ```

3. **Conectar clientes:**
   ```bash
   cd chatp2p
   python client.py
   ```



## Funcionalidades

- ✅ **Comunicação em tempo real** entre múltiplos usuários
- ✅ **Interface interativa** com menu de opções
- ✅ **Proteção de mensagens** (Base64 ou AES)
- ✅ **Suporte multiplataforma** (Windows/Linux/macOS)
- ✅ **Conexão via rede local** - conecte outros computadores
- ✅ **Formatação automática** de mensagens com nome do usuário
- ✅ **Comando `/sair`** para desconectar
- ✅ **Detecção automática de IP** para conexões externas

## Requisitos

- **Python 3.6+** (recomendado Python 3.8+)
- **Sistema operacional:** Windows, Linux ou macOS
- **Biblioteca cryptography** (opcional, só para versão com criptografia AES)

### Instalação do Python
- **Windows:** Baixe em [python.org](https://python.org/downloads/)
- **Linux:** `sudo apt install python3 python3-pip`
- **macOS:** `brew install python3`

## Como conectar outros computadores na rede

1. **🖥️ No computador servidor:**
   - Execute `python server_simple.py` (ou `server.py`)
   - O servidor mostrará o IP para conexão (ex: `192.168.0.173`)

2. **💻 Em outros computadores:**
   - Certifique-se que estão na mesma rede WiFi/LAN
   - Execute `python client_simple.py` (ou `client.py`)
   - Digite o IP mostrado pelo servidor
   - Digite seu nome e comece a conversar!

3. **🔧 Resolução de problemas:**
   - Verifique se o firewall permite conexões na porta 5555
   - Certifique-se que ambos estão na mesma rede
   - Use `127.0.0.1` para testar no mesmo computador

## Comandos disponíveis

- **`/sair`** - Sair do chat
- **`Enter vazio`** - Conectar ao localhost (mesmo PC)
- **`IP do servidor`** - Conectar a outro computador na rede

## Diferenças entre as versões

| Recurso | server_simple.py | server.py |
|---------|------------------|-----------|
| **Proteção** | Codificação Base64 | Criptografia AES |
| **Dependências** | Nenhuma | biblioteca cryptography |
| **Compatibilidade** | ✅ Sempre funciona | ⚠️ Pode ter problemas |
| **Segurança** | 🟡 Básica | 🟢 Avançada |
| **Recomendação** | ✅ Para iniciantes | 🔧 Para usuários avançados |

## Estrutura do projeto

```
chatp2p/
├── server_simple.py      # Servidor com codificação Base64 (recomendado)
├── client_simple.py      # Cliente com codificação Base64 (recomendado)
├── server.py             # Servidor com criptografia AES
├── client.py             # Cliente com criptografia AES
└── README.md
```
