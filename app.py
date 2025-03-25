from flask import Flask, request, jsonify
import yfinance as yf

app = Flask(__name__)

# Route to return your student number
@app.route('/', methods=['GET'])
def home():
    return jsonify({"student_number": "200582212"})

# Webhook route for Dialogflow fulfillment
@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()

    # Get the intent name and parameters
    intent_name = req.get("queryResult", {}).get("intent", {}).get("displayName", "")
    parameters = req.get("queryResult", {}).get("parameters", {})
    stock_symbol = parameters.get("Stock_symbol", "").upper()

    # Debug print to Render logs (optional)
    print("Intent received:", intent_name)
    print("Stock symbol received:", stock_symbol)

    # Check the intent and fetch stock price
    if intent_name == "Get_Stock_Price" and stock_symbol:
        try:
            stock = yf.Ticker(stock_symbol)
            price = stock.history(period="1d")["Close"].iloc[-1]
            response_text = f"The current stock price of {stock_symbol} is ${price:.2f}."
        except Exception as e:
            print("Error fetching stock data:", str(e))
            response_text = f"Sorry, I couldn't fetch the stock price for {stock_symbol}."
    else:
        response_text = "I'm here to assist with trading queries!"

    return jsonify({"fulfillmentText": response_text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
