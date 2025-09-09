from flask import Flask, request, jsonify

app = Flask(__name__)

# Default route (just to check if server works)
@app.route('/')
def home():
    return "Hello, your Flask app is running!"

# Webhook route for Dialogflow
@app.route('/webhook', methods=['POST'])
def webhook():
    # Get request data from Dialogflow
    req = request.get_json(force=True)

    # Extract intent name
    intent = req.get("queryResult").get("intent").get("displayName")

    # Example handling
    if intent == "BookFlight":
        params = req.get("queryResult").get("parameters")
        source = params.get("source-city")
        destination = params.get("destination-city")
        date = params.get("date")

        response_text = f"Booking your flight from {source} to {destination} on {date}."
    else:
        response_text = "I’m not sure what you mean."

    # Return response to Dialogflow
    return jsonify({"fulfillmentText": response_text})


if __name__ == '__main__':
    app.run(debug=True, port=5000)



