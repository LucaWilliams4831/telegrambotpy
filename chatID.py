import requests


TOKEN = "5547844185:AAErY5XVoWU_Av2CH7H-vInZ198IjLeOYaE"

from telethon import TelegramClient, events, sync

# Remember to use your own values from my.telegram.org!
api_id = '2156362'
api_hash = '0d96604bf1fa9092de979309d1606466'
client = TelegramClient('anon', api_id, api_hash)

@client.on(events.NewMessage())
async def my_event_handler(event):
    print(event)

client.start()
client.run_until_disconnected()


#TOKEN = "YOUR TELEGRAM BOT TOKEN"
#chat_id = "618973730"
#message = "hello from your telegram bot"
#url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
#print(requests.get(url).json()) # this sends the message
