## 概要

Discord と LINE で相互にメッセージを送りあう bot (Python) です.  
Heroku で動作させることを想定しています.

## ファイル構成

- `line_bot.py`  
  LINE に送信されたメッセージを Discord に転送します.

- `discord_bot.py`  
  Discord 送信されたメッセージを LINE に転送します.

- `Procfile`, `requirements.txt`, `runtime.txt`  
  Heroku で bot を動作させる際に必要になります.

- `static/hoge`  
  LINE から画像・動画を転送する際に一時的に必要になるフォルダです.  
  任意のファイルを 1 つ以上置いておかないと Heroku で認識されないので `hoge` を置いています.

- `.env`  
  LINE のアクセストークンや Discord の Webhook URL などです.

## 使用方法

各種アカウント, bot の作成は適宜行ってください. (LINE, Discord, LINE Notify, Heroku, GitHub など)

1. `.env` にトークンなどを記載します. これは Heroku 側に設定することもできます.

   - LINE bot のチャンネルアクセストークン
   - LINE bot のチャンネルシークレット
   - Discord の Webhook URL
   - Discord bot のアクセストークン
   - 送信したい LINE のグループ ID (個人で使うならユーザ ID でも OK)
   - Heroku 上でのアプリ名
     <br>
     <br>

1. LINE Webhook には `https://<APP_NAME>.herokuapp.com/callback` を設定してください

1. あとは Heroku で動作させれば OK

## 注意

- 対応しているメッセージは, **テキスト・写真・動画のみ**です.

### Twitter

[@Inahime1006](https://twitter.com/Inahime1006)
