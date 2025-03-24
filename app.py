from flask import Flask, request, jsonify
import yfinance as yf

app = Flask(__name__)

# ✅ Route to return student number
@app.route('/', methods=['GET'])
def home():
    return jsonify({"student_number": "200582212"})  # Replace with your actual student number

# ✅ Webhook route for Dialogflow fulfillment
@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()

    # Extract intent name from Dialogflow request
    intent_name = req.get("queryResult", {}).get("intent", {}).get("displayName")

    # Define responses based on intent
    if intent_name == "Get_Stock_Price":
        parameters = req.get("queryResult", {}).get("parameters", {})
        stock_symbol = parameters.get("stock_symbol", "AAPL")  # Default to AAPL if not provided
        
        try:
            stock = yf.Ticker(stock_symbol)
            price = stock.history(period="1d")["Close"].iloc[-1]
            response_text = f"The current stock price of {stock_symbol.upper()} is ${price:.2f}."
        except Exception as e:
            response_text = f"Sorry, I couldn't fetch the stock price for {stock_symbol}. Please try again."
    
    elif intent_name == "Risk Management":
        response_text = "Risk management involves setting stop-losses and managing portfolio risk."
    
    elif intent_name == "Technical Analysis":
        response_text = "Technical analysis includes price patterns, indicators, and market trends."
    
    elif intent_name == "Trading Strategies":
        response_text = "Trading strategies include scalping, day trading, and swing trading."
    
    else:
        response_text = "I'm here to assist with your trading queries!"

    return jsonify({"fulfillmentText": response_text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
