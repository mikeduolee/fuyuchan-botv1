import os
import random
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

# 模擬盧恩符文資料
runes = [
    {"name": "Fehu", "meaning": "財富、繁榮", "spiritual_guide": "接納富足來到你的生命。", "action_guide": "今天適合整理你的財務或許下關於金錢的願望。"},
    {"name": "Uruz", "meaning": "力量、勇氣", "spiritual_guide": "內在的野性與行動力正在甦醒。", "action_guide": "今天去完成一件你原本畏懼的任務吧。"},
    {"name": "Thurisaz", "meaning": "挑戰、防衛", "spiritual_guide": "挑戰是轉機的入口。", "action_guide": "面對困難，選擇正面迎擊。"},
    {"name": "Ansuz", "meaning": "智慧、溝通", "spiritual_guide": "聆聽內在智慧。", "action_guide": "進行冥想、閱讀或與他人深入交談。"},
    {"name": "Raidho", "meaning": "旅程、變化", "spiritual_guide": "你已準備好啟程。", "action_guide": "今天適合旅行、學習新知或改變習慣。"},
    {"name": "Kenaz", "meaning": "創造、靈感", "spiritual_guide": "你的內在火焰正在燃燒。", "action_guide": "進行創作或解決一直困擾你的問題。"},
    {"name": "Gebo", "meaning": "禮物、連結", "spiritual_guide": "每一次給予都將回到你身上。", "action_guide": "給出你能給的，不計回報。"},
    {"name": "Wunjo", "meaning": "喜悅、和諧", "spiritual_guide": "喜悅來自內心的平衡。", "action_guide": "做一件讓自己發自內心開心的小事。"}
]

def get_daily_rune():
    rune = random.choice(runes)
    return rune["name"], rune["meaning"], rune["spiritual_guide"], rune["action_guide"], "盈月"

@app.route("/")
def hello():
    return "FuYu-chan Bot is running!"

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
    text = event.message.text.strip().lower()
    if text in ["抽", "抽盧恩", "抽一張", "抽一張盧恩", "抽一張符文"]:
        name, meaning, spiritual_guide, action_guide, moon_phase = get_daily_rune()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"🔮 盧恩符文：{name}\n📜 意義：{meaning}\n🔁 正逆位：{'正位' if is_upright else '逆位'}")
意義：{meaning}

🌙 月相：{moon_phase}
📘 指引：
{spiritual_guide}
💡 行動建議：
{action_guide}")
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請輸入『抽』或『抽一張』來獲得今日盧恩指引 🌟")
        )
