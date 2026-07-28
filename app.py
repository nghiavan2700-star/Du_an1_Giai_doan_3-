import os

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from google import genai

# Đọc API key trong file .env
load_dotenv()

app = Flask(__name__)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Không tìm thấy GEMINI_API_KEY trong file .env")

client = genai.Client(api_key=api_key)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(silent=True) or {}
        message = data.get("message", "").strip()

        if not message:
            return jsonify({
                "success": False,
                "reply": "Bạn chưa nhập câu hỏi."
            }), 400

        prompt = f"""
Bạn là trợ lý AI thân thiện dành cho sinh viên.

Yêu cầu:
- Luôn trả lời bằng tiếng Việt.
- Trả lời rõ ràng, dễ hiểu và không quá dài.
- Chỉ sử dụng tiếng Anh khi người dùng yêu cầu.
- Không tự tạo thông tin khi không chắc chắn.

Câu hỏi của người dùng:
{message}
"""

        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt
        )

        answer = response.text or "Xin lỗi, tôi chưa thể trả lời câu hỏi này."

        return jsonify({
            "success": True,
            "reply": answer
        })

    except Exception as error:
        print("Lỗi:", error)

        return jsonify({
            "success": False,
            "reply": "Không thể kết nối với AI. Bạn hãy thử lại."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)