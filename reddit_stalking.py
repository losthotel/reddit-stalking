import os
import time
import threading
import random
from collections import deque
from dotenv import load_dotenv
import praw
import requests
from email.message import EmailMessage
import smtplib

load_dotenv()

CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
USER_AGENT = os.getenv("REDDIT_USER_AGENT", "WatcherBot/0.1")
TARGET_USER = os.getenv("TARGET_USER")
SUBREDDITS = os.getenv("SUBREDDITS", "all")  # lista separada por +
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK_URL")
EMAIL_NOTIFY = os.getenv("EMAIL_NOTIFY", "false").lower() == "true"

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
TO_EMAIL = os.getenv("TO_EMAIL")

SEEN_MAX = 5000
seen = deque(maxlen=SEEN_MAX)
seen_set = set()

item_counter = 0

reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT,
    check_for_async=False
)

# ------------------- Notificações -------------------
def notify_discord(content: str):
    if not DISCORD_WEBHOOK:
        return
    data = {"content": content}
    try:
        resp = requests.post(DISCORD_WEBHOOK, json=data, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        print("Erro webhook:", e)

def notify_email(subject: str, body: str):
    if not EMAIL_NOTIFY:
        return
    msg = EmailMessage()
    msg["From"] = SMTP_USER
    msg["To"] = TO_EMAIL
    msg["Subject"] = subject
    msg.set_content(body)
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=20) as s:
            s.starttls()
            s.login(SMTP_USER, SMTP_PASS)
            s.send_message(msg)
    except Exception as e:
        print("Erro SMTP:", e)

# ------------------- Manipulação de posts/comentários -------------------
def handle_item(item, kind):
    global item_counter
    author = getattr(item.author, "name", None)
    if not author or author.lower() != TARGET_USER.lower():
        return

    item_id = f"{kind}_{item.id}"
    if item_id in seen_set:
        return
    seen.append(item_id)
    seen_set.add(item_id)

    permalink = getattr(item, "permalink", None)
    url = f"https://reddit.com{permalink}" if permalink else getattr(item, "url", "")
    title = getattr(item, "title", "") if kind == "submission" else ""
    
    kind_name = "postagem" if kind == "submission" else "comentário"

    created = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime(item.created_utc))
    content = f"**{TARGET_USER}** postou no r/{item.subreddit.display_name} ({kind_name}) em {created}\n{title}\n{url}"

    print("Detectado:", content)
    notify_discord(content)
    if EMAIL_NOTIFY:
        notify_email(f"{TARGET_USER} postou no r/{item.subreddit.display_name}", content)

    time.sleep(random.uniform(1, 3))
    item_counter += 1

    if item_counter % 30 == 0:
        print("Pausa de segurança: 3 minutos para evitar comportamento suspeito...")
        time.sleep(180)

# ------------------- Histórico dos últimos 7 dias -------------------
def fetch_last_week_subreddits(subreddits_str):
    one_week_ago = time.time() - 7*24*60*60
    subs = [s.strip() for s in subreddits_str.split("+") if s.strip()]
    for sub_name in subs:
        print(f"Buscando no r/{sub_name}...")
        subreddit = reddit.subreddit(sub_name)
        try:

            for submission in subreddit.new(limit=2000):
                if submission.created_utc < one_week_ago:
                    break
                handle_item(submission, "submission")

            for comment in subreddit.comments(limit=2000):
                if comment.created_utc < one_week_ago:
                    break
                handle_item(comment, "comment")
        except Exception as e:
            print(f"Erro ao buscar em r/{sub_name}: {e}")

        time.sleep(random.uniform(2, 5))

# ------------------- Monitoramento em tempo real -------------------
def stream_submissions(subreddits_str):
    multis = "+".join([s.strip() for s in subreddits_str.split("+") if s.strip()])
    subreddit = reddit.subreddit(multis)
    for submission in subreddit.stream.submissions(skip_existing=True):
        try:
            handle_item(submission, "submission")
            time.sleep(600)
        except Exception as e:
            print("Erro ao processar submission:", e)

def stream_comments(subreddits_str):
    multis = "+".join([s.strip() for s in subreddits_str.split("+") if s.strip()])
    subreddit = reddit.subreddit(multis)
    for comment in subreddit.stream.comments(skip_existing=True):
        try:
            handle_item(comment, "comment")
            time.sleep(600)
        except Exception as e:
            print("Erro ao processar comment:", e)

# ------------------- Main -------------------
if __name__ == "__main__":
    if not CLIENT_ID or not CLIENT_SECRET or not USER_AGENT or not TARGET_USER:
        print("Preencha as variáveis no .env (client id/secret/useragent/target).")
        raise SystemExit(1)

    print(f"Buscando posts/comentários dos últimos 7 dias de {TARGET_USER} nos subreddits listados...")
    fetch_last_week_subreddits(SUBREDDITS)
    print("Busca histórica concluída. Iniciando monitoramento em tempo real...")

    t1 = threading.Thread(target=stream_submissions, args=(SUBREDDITS,), daemon=True)
    t2 = threading.Thread(target=stream_comments, args=(SUBREDDITS,), daemon=True)
    t1.start()
    t2.start()

    print(f"Monitorando subreddits listados por posts/comentários do usuário {TARGET_USER}...")
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("Saindo...")
