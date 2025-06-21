from telethon import TelegramClient, events
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
from telethon.sessions import StringSession
import os
import asyncio

# Carregar variáveis do .env
load_dotenv()

# Telegram
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
session_string = os.getenv("SESSION_STRING")
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
client = TelegramClient(StringSession(session_string), api_id, api_hash)

@client.on(events.NewMessage)
async def monitorar_mensagem(event):
    if frase_chave.lower() in event.raw_text.lower():
        print(f"🔍 Frase detectada: {event.raw_text}")
        enviar_email(f"Mensagem encontrada no Telegram:\n\n{event.raw_text}")

# Função principal assíncrona
async def main():
    print("✅ Conectando ao Telegram...")
    await client.connect()  
    print("🔔 Monitoramento iniciado. Aguardando mensagens...")
    await client.run_until_disconnected()

# Início do programa
asyncio.run(main())
