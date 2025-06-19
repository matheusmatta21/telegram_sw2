from telethon import TelegramClient, events
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

# Carregar variáveis do .env
load_dotenv()

# Telegram
print(("API_ID:", os.getenv("API_ID")))
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
phone_number = os.getenv("PHONE_NUMBER")
frase_chave = "Nintendo Switch 2"

# E-mail
email_origem = os.getenv("EMAIL_ORIGEM")
email_senha = os.getenv("EMAIL_SENHA")
email_destino = os.getenv("EMAIL_DESTINO")

# Função para enviar e-mail
def enviar_email(mensagem):
    msg = MIMEText(mensagem)
    msg['Subject'] = '⚠️ Palavra-chave encontrada no Telegram!'
    msg['From'] = email_origem
    msg['To'] = email_destino

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email_origem, email_senha)
            smtp.send_message(msg)
            print("E-mail enviado!")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

# Criar cliente do Telegram
client = TelegramClient('monitor', api_id, api_hash)

@client.on(events.NewMessage)
async def monitorar_mensagem(event):
    if frase_chave.lower() in event.raw_text.lower():
        print(f"🔍 Frase detectada: {event.raw_text}")
        enviar_email(f"Mensagem encontrada no Telegram:\n\n{event.raw_text}")

print("✅ Iniciando monitoramento...")
client.start(phone=phone_number)
print("🔔 Monitoramento iniciado. Aguardando mensagens...")
client.run_until_disconnected()