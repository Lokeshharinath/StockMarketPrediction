# Stock Prediction App

The Stock Prediction App is a web application that predicts stock prices based on historical data using a Long Short-Term Memory (LSTM) model. This application provides users with a user-friendly interface to input stock symbols, forecast periods, and historical years to receive predictions and visualizations.

## Features

- Predict stock prices for given stock symbols.
- Select forecast periods (e.g., 30 days, 6 months, 1 year).
- Input historical years to consider for the prediction.
- Display loading GIF while fetching predictions.
- Show detailed results including current price, projected profit/loss, and a prediction plot.
- Responsive design for better usability on different devices.

## Installation

To run the Stock Prediction App locally, follow these steps:

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/stock-prediction-app.git
    cd stock-prediction-app
    ```

2. **Create a virtual environment and activate it:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the application:**

    ```bash
    python app.py
    ```

5. **Open your browser and navigate to:**

    ```
    http://127.0.0.1:5000
    ```

## Project Structure

- **app.py**: The main Flask application file that handles routing and predictions.
- **static/**: Contains static files like CSS, JavaScript, and images.
  - `styles.css`: The main stylesheet for the application.
  - `script.js`: JavaScript for handling form submissions and dynamic content.
  - `loading.gif`: GIF displayed while fetching data.
- **templates/**: Contains HTML templates.
  - `index.html`: Home page.
  - `about.html`: About page.
  - `contact.html`: Contact page.
  - `predict.html`: Prediction page.
- **requirements.txt**: Lists all the dependencies required to run the application.

## Usage

1. Navigate to the prediction page.
2. Enter a stock symbol (e.g., AAPL for Apple Inc.).
3. Select the forecast period and the number of historical years to consider.
4. Click the "Predict" button.
5. Wait for the prediction to load. The results will display the current price, projected profit/loss, and a prediction plot.

## Contributing

Contributions are welcome! If you would like to contribute to this project, please fork the repository and submit a pull request.

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or feedback, please contact:

- **Name**: Gonthina Lokesh Harinath
- **Email**: glharinath1998@gmail.com
- **LinkedIn**: [linkedin.com/in/lokesh-harinath-a8b21b195](https://linkedin.com/in/lokesh-harinath-a8b21b195)

---

Happy predicting!
