import os

from linebot.models import *
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError


app = Flask(__name__)

Channel_Access_Token = ''
line_bot_api    = LineBotApi(Channel_Access_Token)
Channel_Secret  = ''
handler = WebhookHandler(Channel_Secret)

# handle request from "/callback" 
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body      = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# handle text message
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    if event.source.user_id != " ":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=msg)
        )

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
