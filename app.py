from flask import Flask, request, jsonify
import os
from groq import Groq   # pip install groq

app = Flask(__name__)

# Initialize Groq client (make sure GROQ_API_KEY is set in Render environment variables)
client = Groq(api_key=os.environ.get("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"))

@app.route('/')
def home():
    return "Flask app running with AI responses!"

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(force=True)
    intent = req.get("queryResult").get("intent").get("displayName")
    user_message = req.get("queryResult").get("queryText")

    # Default prompt
    prompt = f"You are a helpful AI assistant. User asked: {user_message}"

    if intent == "get_overview":
        prompt = f"Give a simple overview explanation about {user_message}."
    elif intent == "get_detail":
        prompt = f"Explain in detail about {user_message}."
    elif intent == "next_topic":
        prompt = f"Suggest the next topic the user should learn after {user_message}."

    # Call Groq LLM
    response = client.chat.completions.create(
        model="llama3-8b-8192",   # choose Groq model
        messages=[
            {"role": "system", "content": "You are an AI assistant that answers clearly."},
            {"role": "user", "content": prompt}
        ],
    )

    ai_text = response.choices[0].message.content

    return jsonify({"fulfillmentText": ai_text})

if __name__ == '__main__':
    app.run(debug=True, port=5000)

