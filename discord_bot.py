import discord
import dotenv
import os
import requests

client = discord.Client()

# 環境変数取得
dotenv.load_dotenv()
DISCORD_ACCESS_TOKEN = os.environ['DISCORD_ACCESS_TOKEN']
LINE_NOTIFY_TOKEN = os.environ['LINE_NOTIFY_TOKEN']


@client.event
async def on_message(message):
    # bot からのメッセージは無視する
    if message.author.bot:
        return

    if len(message.content) != 0:
        if len(message.attachments) != 0:
            length = len(message.attachments)
            content = '\n' + message.author.display_name + \
                ': \n' + message.content + '\nFile URL:'
            for i in range(length):
                content += ('\n\n' + message.attachments[i].url)
            file = {
                'message': content
            }
            return send_message(file)
        else:
            file = {
                'message': '\n' + message.author.display_name + ': \n\n' + message.content
            }
            return send_message(file)
    else:
        if len(message.attachments) != 0:
            length = len(message.attachments)
            content = '\n' + message.author.display_name + ': \n\n' + '\nFile URL:'
            for i in range(length):
                content += ('\n\n' + message.attachments[i].url)
            file = {
                'message': content
            }
            return send_message(file)
        else:
            return


def send_message(file):

    headers = {
        'Authorization': 'Bearer ' + LINE_NOTIFY_TOKEN,
    }
    files = file
    requests.post('https://notify-api.line.me/api/notify',
                  headers=headers, data=files)


client.run(DISCORD_ACCESS_TOKEN)
