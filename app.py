import os
import random
from flask import Flask, request, abort, send_from_directory
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
from datetime import datetime
import pytz

app = Flask(__name__)

# 環境變數設定
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

# 所有盧恩符文與對應解釋（部分示範，可補足）
runes = [
    {
        "name": "Fehu",
        "image": "fehu",
        "meaning_upright": ["你擁有創造財富的能力。", "現在是為夢想播種的好時機。"],
        "action_upright": ["規劃你的資源使用。", "採取具體的行動去實現目標。"],
        "meaning_reversed": ["能量正在流失，需重新審視。", "注意財務或關係上的耗損。"],
        "action_reversed": ["避免衝動花費。", "給自己空間反思真正需求。"]
    },
    {
        "name": "Uruz",
        "image": "uruz",
        "meaning_upright": ["你擁有內在的力量與勇氣。", "是突破困境的時機。"],
        "action_upright": ["信任自己的決定。", "做出需要勇氣的選擇。"],
        "meaning_reversed": ["力量可能被誤用或壓抑。", "注意身心健康的失衡。"],
        "action_reversed": ["釋放內在壓力。", "尋找支持，重新找回節奏。"]
    }
]

def draw_rune():
    rune = random.choice(runes)
    is_reversed = random.choice([True, False])
    direction = "reversed" if is_reversed else "upright"
    meaning = random.choice(rune[f"meaning_{direction}"])
    action = random.choice(rune[f"action_{direction}"])
    image_url = f"https://{os.getenv('RAILWAY_STATIC_URL', 'example.com')}/static/images/{rune['image']}_{direction}.png"
    return rune["name"], image_url, meaning, action

@app.route("/")
def home():
    return "FuYu-chan v7 is running."

@app.route("/webhook", methods=["POST"])
def webhook():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text.strip()

    if text in ["抽", "抽一張", "抽盧恩"]:
        name, image, meaning, action = draw_rune()
        line_bot_api.reply_message(event.reply_token, [
            ImageSendMessage(original_content_url=image, preview_image_url=image),
            TextSendMessage(text=f"🔮 盧恩符文：{name}

🌿 心靈指引：{meaning}

🔨 行動建議：{action}")
        ])
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請輸入「抽」、「抽一張」或「抽盧恩」來抽卡喔～"))

@app.route("/static/images/<path:filename>")
def static_files(filename):
    return send_from_directory("static/images", filename)
