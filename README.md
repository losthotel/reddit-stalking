# 👁️ Reddit Stalker BOT
<p align="center">
  <img src="evilreddit.png" width="200">
</p>

Um bot de monitoramento que **vigia atividades de um usuário específico do Reddit** (posts e comentários) em **subreddits escolhidos**, enviando **notificações automáticas para o Discord** (via Webhook) e/ou **e-mail**.

---

## ⚙️ Funcionalidades

- Monitora **postagens e comentários** de um usuário definido (`TARGET_USER`);
- Suporte a **múltiplos subreddits** (ex: `gta+minecraft+desabafos`);
- Envia **notificações para um canal do Discord** via Webhook;
- Envia **alertas por e-mail** (opcional);
- Realiza uma **busca inicial** dos últimos 7 dias antes de iniciar o monitoramento em tempo real;
- Pausas automáticas e limites de segurança para **evitar banimento da conta BOT**;
- Configuração simples via **.env**.

---

## 🧩 Instalação

### 1️⃣ Clonar o repositório
```bash
git clone https://github.com/losthotel/reddit-stalking.git
cd reddit-stalking
```

### 2️⃣ Criar o ambiente virtual (opcional, mas recomendado)
```bash
python -m venv venv
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate     # Windows
```

### 3️⃣ Instalar as dependências
```bash
pip install -r requirements.txt
```

---

## 🔑 Configuração (.env)

```env
REDDIT_CLIENT_ID=seu_client_id         # ID do App criado no Reddit
REDDIT_CLIENT_SECRET=seu_client_secret # Secret do App
REDDIT_USER_AGENT=WatcherBot/0.1 por u/SeuNome
TARGET_USER=usuario_a_monitorar        # Ex: GameMaster123
SUBREDDITS=gta+minecraft+desabafos     # Subreddits separados por '+'
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...   # Webhook do canal
EMAIL_NOTIFY=false                     # true para ativar e-mails

# Configuração do SMTP (caso EMAIL_NOTIFY = true)
SMTP_SERVER=smtp.exemplo.com
SMTP_PORT=587
SMTP_USER=seu@email.com
SMTP_PASS=sua_senha
TO_EMAIL=destino@email.com
```

---

## 🧠 Criando o App no Reddit

1. Vá para: [https://www.reddit.com/prefs/apps](https://www.reddit.com/prefs/apps)  
2. Clique em **"Create another app..."**  
3. Dê um nome (ex: `WatcherBot`)  
4. Tipo: **script**  
5. Adicione uma **redirect URI** (pode ser `http://localhost:8080`)  
6. Após criar, copie o:
   - **Client ID** (logo abaixo do nome do app)
   - **Client Secret** (na seção “secret”)  
   E coloque no `.env`

---

## 🚀 Como rodar

```bash
python reddit_stalking.py
```

O bot exibirá no console:
```
Buscando posts/comentários dos últimos 7 dias de usuario...
Busca histórica concluída. Iniciando monitoramento em tempo real...
Monitorando subreddits listados...
```

### 🧭 O que ele faz:
- Busca atividades recentes do usuário nos subreddits informados.
- Depois, inicia o monitoramento em tempo real:
  - Ao detectar uma nova postagem ou comentário do usuário,
  - Envia automaticamente uma notificação no Discord e/ou e-mail.

---

## 🪄 Exemplo de mensagem no Discord

```
**GameMaster123** postou no r/gta (comentário) em 19/10/2025 12:47:00
Esse mod é incrível!
https://reddit.com/r/gta/comments/abc123/
```

---

## 🧱 Dicas de segurança

- **Evite reduzir o intervalo de tempo entre requisições.** O script já respeita pausas automáticas (1–3 segundos entre ações e 3 min a cada 30 notificações). Alterar o intervalo de tempo pode resultar em banimento do Reddit.
- **Use um bot secundário** (não sua conta principal).
- Não abuse de múltiplas execuções simultâneas.
- **Nunca compartilhe** seu `.env` público (contém tokens e senhas).

---

## 🧰 Compatibilidade

- Python **3.9+**
- Sistemas: **Windows / Linux / macOS**

---

## 📜 Licença

Este projeto é distribuído sob a licença **MIT**.  
Sinta-se livre para modificar e usar com os devidos créditos.

---

## 💡 Créditos

Desenvolvido por **Losthotel**  
🔗 Projeto: [GitHub](https://github.com/losthotel/reddit-stalking)
