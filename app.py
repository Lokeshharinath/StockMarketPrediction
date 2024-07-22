from flask import Flask, render_template, request, jsonify
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import random
import matplotlib.pyplot as plt
import base64
from io import BytesIO

app = Flask(__name__)

def set_random_seeds(seed_value=42):
    np.random.seed(seed_value)
    tf.random.set_seed(seed_value)
    random.seed(seed_value)

def get_stock_data(symbol, start_date, end_date):
    stock_data = yf.download(symbol, start=start_date, end=end_date)
    return stock_data

def prepare_data(data, n_steps):
    x, y = [], []
    for i in range(len(data) - n_steps):
        x.append(data[i:(i + n_steps), 0])
        y.append(data[i + n_steps, 0])
    return np.array(x), np.array(y)

def create_lstm_model(input_shape):
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=input_shape))
    model.add(LSTM(units=50))
    model.add(Dense(units=1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def predict_stock_prices(symbol, forecast_period, historical_years):
    set_random_seeds()
    end_date = pd.Timestamp.now().strftime('%Y-%m-%d')
    start_date = (pd.Timestamp.now() - pd.DateOffset(years=historical_years)).strftime('%Y-%m-%d')

    stock_data = get_stock_data(symbol, start_date=start_date, end_date=end_date)
    closing_prices = stock_data['Close'].values.reshape(-1, 1)
    scaler = MinMaxScaler(feature_range=(0, 1))
    closing_prices_scaled = scaler.fit_transform(closing_prices)

    if len(closing_prices_scaled) == 0:
        return None, "No data available for the provided symbol."

    n_steps = 60
    x_train, y_train = prepare_data(closing_prices_scaled, n_steps)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    model = create_lstm_model((x_train.shape[1], 1))
    model.fit(x_train, y_train, epochs=10, batch_size=32)

    forecast_data = closing_prices_scaled[-n_steps:].copy()
    forecast = []
    for _ in range(forecast_period):
        forecast_input = np.reshape(forecast_data, (1, n_steps, 1))
        next_price_scaled = model.predict(forecast_input)[0][0]
        forecast.append(next_price_scaled)
        forecast_data = np.append(forecast_data[1:], [[next_price_scaled]], axis=0)

    forecast = scaler.inverse_transform(np.array(forecast).reshape(-1, 1))
    current_price = closing_prices[-1][0]  # Get the last closing price from the data
    next_forecast = forecast[-1][0]
    profit_loss_next_forecast = next_forecast - current_price

    plt.figure(figsize=(12, 6))
    plt.plot(stock_data.index, closing_prices, label='Actual Prices', color='blue')
    plt.plot(pd.date_range(start=stock_data.index[-1] + pd.Timedelta(days=1), periods=forecast_period), forecast, label='Forecasted Prices', color='red')
    plt.title(f'{symbol} Stock Price Forecast for {forecast_period} days using LSTM')
    plt.xlabel('Date')
    plt.ylabel('Stock Price (USD)')
    plt.legend()
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    image_base64 = base64.b64encode(image_png).decode('utf-8')

    return profit_loss_next_forecast, image_base64, current_price

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/predict')
def predict():
    return render_template('predict.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/predict_stock', methods=['POST'])
def predict_stock():
    data = request.json
    symbol = data.get('symbol', '').upper()
    forecast_period = data.get('forecast_period', '30days')
    historical_years = int(data.get('historical_years', 1))

    forecast_days = 30  # Default to 30 days
    if forecast_period == '6months':
        forecast_days = 6 * 30
    elif forecast_period == '1year':
        forecast_days = 12 * 30

    profit_loss, plot_url, current_price = predict_stock_prices(symbol, forecast_days, historical_years)

    if profit_loss is None:
        return jsonify({'error': "No data available for the provided symbol."})

    return jsonify({
        'symbol': symbol,
        'forecast_period': forecast_period,
        'profit_loss': float(profit_loss),
        'plot_url': plot_url,
        'current_price': float(current_price)
    })

if __name__ == '__main__':
    app.run(debug=True)
