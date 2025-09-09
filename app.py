from flask import Flask, request, jsonify
import os
from groq import Groq

app = Flask(__name__)

# Initialize Groq client
api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    raise ValueError("❌ GROQ_API_KEY is not set. Please configure it in Render Environment variables.")

client = Groq(api_key=api_key)

@app.route('/')
def home():
    return "Flask app running with AI responses!"

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(force=True)
    intent = req.get("queryResult", {}).get("intent", {}).get("displayName", "")
    user_message = req.get("queryResult", {}).get("queryText", "")

    if not user_message:
        return jsonify({"fulfillmentText": "⚠️ I didn’t get any input."})

    # Decide prompt based on intent
    if intent == "get_overview":
        prompt = f"Give a simple overview explanation about {user_message}."
    elif intent == "get_detail":
        prompt = f"Explain in detail about {user_message}."
    elif intent == "next_topic":
        prompt = f"Suggest the next topic the user should learn after {user_message}."
    else:
        prompt = f"You are a helpful AI assistant. User asked: {user_message}"

    try:
        # Call Groq API
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "You are an AI assistant that answers clearly."},
                {"role": "user", "content": prompt}
            ],
        )

        ai_text = response.choices[0].message.content
        return jsonify({"fulfillmentText": ai_text})

    except Exception as e:
        # Capture error gracefully
        return jsonify({"fulfillmentText": f"⚠️ Error: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)

  
