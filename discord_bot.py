import discord
import dotenv
import json
import os
import requests

client = discord.Client()

# Discord, LINE, Group ID
dotenv.load_dotenv()
CHANNEL_ACCESS_TOKEN = os.environ['CHANNEL_ACCESS_TOKEN']
DISCORD_ACCESS_TOKEN = os.environ['DISCORD_ACCESS_TOKEN']
LINE_GROUP_ID = os.environ['LINE_GROUP_ID']


@client.event
async def on_message(message):
    # bot からのメッセージは無視する
    if message.author.bot:
        return

    post_to_line(message)


def post_to_line(msg):
    content = format_content(msg)
    message = {
        'to': LINE_GROUP_ID,
        'messages': content
    }

    headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer ' + CHANNEL_ACCESS_TOKEN}

    requests.post('https://api.line.me/v2/bot/message/push',
                  data=json.dumps(message), headers=headers)


def format_content(message):
    content = [
        {
            'type': 'text',
            'text': message.author.display_name + ' sent on Discord'
        }
    ]

    if len(message.content) != 0:
        content.append(
            {'type': 'text',
             'text': message.content},
        )

    if len(message.attachments) != 0:
        roop = len(message.attachments)
        for i in range(roop):
            content_type = message.attachments[i].content_type
            if 'image' in content_type:
                content.append(
                    {'type': 'image',
                     'originalContentUrl': message.attachments[i].url,
                     'previewImageUrl': message.attachments[i].url}
                )
            elif 'video' in content_type:
                content.append(
                    {'type': 'video',
                     'originalContentUrl': message.attachments[i].url,
                     'previewImageUrl': message.attachments[i].url}
                )

    return content


client.run(DISCORD_ACCESS_TOKEN)
