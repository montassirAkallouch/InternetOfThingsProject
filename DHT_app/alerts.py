import vonage
from django.conf import settings
from django.core.mail import send_mail
from telegram import Bot
import asyncio
import requests


def telegram_alert(message, targetToken):
    async def send_telegram_message(token, chat_id, message_text):
        bot = Bot(token=token)
        await bot.send_message(chat_id=chat_id, text=message_text)

    bot_token = targetToken
    chat_id = '6645144819'
    message_text = message

    asyncio.run(send_telegram_message(bot_token, chat_id, message_text))


def email_alert(message, email):
    subject = 'Alerte DHT'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = list()
    recipient_list.append(email)
    send_mail(subject, message, email_from, recipient_list)


def sms_alert(message, number):
    client = vonage.Client(key="d85546ac", secret="0ZmzM12F2JkmoreA")
    client.sms.send_message(
        {
            "from": "IOT_DHT_APP",
            "to": number,
            "text": message,
        }
    )


def wtsp_alert(message, number):
    url = "https://messages-sandbox.nexmo.com/v1/messages"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    auth = ("d85546ac", "0ZmzM12F2JkmoreA")
    data = {
        "from": "14157386102",
        "to": number,
        "message_type": "text",
        "text": message,
        "channel": "whatsapp",
    }
    response = requests.post(url, headers=headers, auth=auth, json=data)

