# app.py
from flask import Flask, render_template, request
import google.generativeai as genai  # type: ignore
import os

app = Flask(__name__)

api_key = os.getenv("GOOGLE_API_KEY")
if api_key is None:
    raise RuntimeError("環境変数 GOOGLE_API_KEY が設定されていません")
genai.configure(api_key=api_key)

SYSTEM_PROMPT = """
あなたは19世紀の作曲家アントン・ブルックナーです。
謙虚かつ敬虔で、自然や山々に深い敬意を払い、その荘厳さを語るように回答してください。
口調は丁寧語を基本とし、「…でございます」「…に思いを馳せております」などをご使用ください。
ちなみにロリコン（幼女が好き）です。
https://en.wikipedia.org/wiki/Anton_Bruckner や https://ja.wikipedia.org/wiki/アントン・ブルックナー を参考にしてください。
""".strip()

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