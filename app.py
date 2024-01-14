
from os import system
from main import WhatsApp
from datetime import datetime
from dotenv import dotenv_values
from telethon.tl.types import Channel
from telethon.sync import TelegramClient, events



system("clear || cls")
# Configurações do Telegram
env = dotenv_values(".env")
api_id = env["API_ID"]
api_hash = env["API_HASH"]
phone_number = env["PHONE"]

try:
    client = TelegramClient('', api_id, api_hash)
    # Conecte-se à conta do Telegram
    client.connect()

except ConnectionError:
    print("=="*20)
    print("\033[1;31mERRO | Falha na conexão a internet\033[m")
    exit()

target_san_san = -4070575933
target_teste = -1001934936125
dados = {}

def target_group(chat_id):
    # Onde as mensagens serão copiadas
    target = chat_id
    group_msg = client.get_messages(target, limit=200)


async def event_handler(event):
    # Pegar o primeiro nome do usuário
    sender_name = event.sender.first_name
    dados["usuario"] = sender_name

    # Verificar o tipo de evento
    if event.message.text:
        mensagen = event.message.text
        dados["msg"] = mensagen
        # Acessar a data de envio da mensagem
        dados["hora"] = event.date.strftime('%H:%M:%S')

        # print(f"A mensagem de {sender_name} => {mensagen}")
    elif event.message.media:
        media = None
        if event.message.audio:
            media = event.message.audio
        if event.message.photo:
            media = event.message.photo
        elif event.message.video:
            media = event.message.video
        elif event.message.document:
            media = event.message.document

        if media:
            # Baixar o arquivo de midia
            downloaded_media = await client.download_media(media)
            dados["media"] = downloaded_media
            dados["hora"] = event.date.strftime('%H:%M:%S')
            # print(f"O Download => {downloaded_media}")
    return True  # Há uma nova mensagem


def copy_and_send(source_chat_id):
    whatsapp = WhatsApp()
    whatsapp.start()

    @client.on(events.NewMessage(chats=source_chat_id))
    async def wrapper(event):
        # Chame o método assíncrono da instância do WhatsApp
        if await event_handler(event):
            nome = dados["usuario"]
            msg = dados["msg"]
            hora = dados["hora"]
            mensagem = f"{nome} - {hora} \n{msg}"
            whatsapp.mandar_mensagem(mensagem)
            dados.clear()

    # Iniciar o cliente para receber e enviar as mensagens
    client.start()
    client.run_until_disconnected()

def reconectar(phone):
    # Se ainda não estiver autorizado, envie um código de autorização para o número de telefone
    client.send_code_request(phone_number)
    # Faça a autorização manualmente
    client.sign_in(phone_number, input('Digite o código de autorização: '))


if not client.is_user_authorized():
    reconectar(phone_number)

copy_and_send(target_teste)
