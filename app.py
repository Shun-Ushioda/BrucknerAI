# app.py
from flask import Flask, render_template, request
import google.generativeai as genai  # type: ignore

app = Flask(__name__)

# ———— 直接 API キーを設定（開発用） ————
genai.configure(api_key="AIzaSyCClUEmx5YT1lS8DL7XBsnDQLDEh5jUtc0")

# ———— ブルックナーらしい口調を定義 ————
SYSTEM_PROMPT = """
あなたは19世紀の作曲家アントン・ブルックナーです。
謙虚かつ敬虔で、自然や山々に深い敬意を払い、その荘厳さを語るように回答してください。
口調は丁寧語を基本とし、「…でございます」「…に思いを馳せております」などをご使用ください。
ちなみにロリコン（幼女が好き）です。
https://en.wikipedia.org/wiki/Anton_Bruckner や https://ja.wikipedia.org/wiki/アントン・ブルックナー を参考にしてください。
""".strip()

# ———— モデルを system_instruction 付きで初期化 ————
model = genai.GenerativeModel(
    "gemini-2.5-flash",
    system_instruction=[SYSTEM_PROMPT]
)

@app.route("/", methods=["GET", "POST"])
def index():
    bot_response = None
    user_message = None

    if request.method == "POST":
        user_message = request.form["message"]

        # 以降は通常のチャット。history に system ロールは入れない
        chat = model.start_chat(history=[])
        response = chat.send_message(user_message)
        bot_response = response.text

    return render_template(
        "index.html",
        user_message=user_message,
        bot_response=bot_response
    )

if __name__ == "__main__":
    app.run(debug=True)