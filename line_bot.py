import os
import dotenv
import requests

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, ImageMessage, VideoMessage
)

app = Flask(__name__)


# 環境変数取得
dotenv.load_dotenv()
CHANNEL_ACCESS_TOKEN = os.environ['CHANNEL_ACCESS_TOKEN']
CHANNEL_SECRET = os.environ['CHANNEL_SECRET']
DISCORD_WEBHOOK_URL = os.environ['DISCORD_WEBHOOK_URL']
APP_NAME = os.environ['APP_NAME']

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

FQDN = 'https://' + APP_NAME + '.herokuapp.com'


# Webhookからのリクエストの署名検証部分
@app.route('/callback', methods=['POST'])
def callback():
    # 署名検証のための値
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info('Request body: ' + body)

    # 署名検証
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print('Invalid signature. Please check your channel access token/channel secret.')
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    send_user_id = event.source.user_id
    profile = line_bot_api.get_profile(send_user_id)

    post_text_discord_webhook(event, profile)


@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    send_user_id = event.source.user_id
    profile = line_bot_api.get_profile(send_user_id)

    message_content = line_bot_api.get_message_content(event.message.id)
    with open('static/' + event.message.id + '.jpg', 'wb') as f:
        f.write(message_content.content)
        original_content_url = FQDN + '/static/' + event.message.id + '.jpg'
        post_media_discord_webhook(profile, original_content_url)


@handler.add(MessageEvent, message=VideoMessage)
def handle_video_message(event):
    send_user_id = event.source.user_id
    profile = line_bot_api.get_profile(send_user_id)

    message_content = line_bot_api.get_message_content(event.message.id)
    with open('static/' + event.message.id + '.mp4', 'wb') as f:
        f.write(message_content.content)
        original_content_url = FQDN + '/static/' + event.message.id + '.mp4'
        post_media_discord_webhook(profile, original_content_url)


def post_text_discord_webhook(event, profile):
    main_content = {
        'username': profile.display_name,
        'avatar_url': profile.picture_url,
        'content': event.message.text
    }

    requests.post(DISCORD_WEBHOOK_URL, main_content)


def post_media_discord_webhook(profile, url):
    main_content = {
        'username': profile.display_name,
        'avatar_url': profile.picture_url,
        'content': url
    }

    requests.post(DISCORD_WEBHOOK_URL, main_content)


if __name__ == '__line_bot__':
    app.run(port=5000)
