from flask import Flask, request, jsonify
import yfinance as yf

app = Flask(__name__)

@app.route("/")
def home():
   return "Flask API is running"

@app.route("/stock-data", methods = ['GET'])
def getRealTimeStockInfo():
    symbol = request.args.get('symbol')

    if not symbol:
        return jsonify({"error": "Please provide a company symbol"}), 400

    try:
        stock = yf.Ticker(symbol)
        info = stock.info

        current_price = info.get("currentPrice")
        previous_close = info.get("previousClose")

        if current_price and previous_close:
            change = current_price - previous_close
            percent_change = (change / previous_close) * 100
        else:
            change = None
            percent_change = None

        data = {
            "symbol": symbol.upper(),
            "market_state": info.get("marketState"),
            "current_price": current_price,
            "price_change": change,
            "percentage_change": percent_change
        }

        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

