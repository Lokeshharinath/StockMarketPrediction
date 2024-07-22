// script.js

document.getElementById('prediction-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const symbol = document.getElementById('symbol').value.trim();
    const forecastPeriod = document.getElementById('forecast-period').value;
    const historicalYears = document.getElementById('historical-years').value;

    // Clear previous results and error messages
    clearResult();

    // Show loading GIF
    document.getElementById('loading').style.display = 'block';

    try {
        const response = await fetch('/predict_stock', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                symbol: symbol,
                forecast_period: forecastPeriod,
                historical_years: historicalYears
            })
        });

        const result = await response.json();

        // Hide loading GIF after fetching data
        document.getElementById('loading').style.display = 'none';

        if (response.ok) {
            // Display results
            displayResult(result);
        } else {
            // Display error message
            displayError(result.error || 'An unexpected error occurred. Please try again.');
        }
    } catch (error) {
        // Hide loading GIF
        document.getElementById('loading').style.display = 'none';
        // Display error message
        displayError('Failed to fetch data. Please check your network connection and try again.');
    }
});

function displayResult(result) {
    document.getElementById('result-symbol').innerText = `Symbol: ${result.symbol}`;
    document.getElementById('current-price').innerText = `Current Price: $${result.current_price.toFixed(2)}`;
    document.getElementById('result-profit-loss').innerText = `Projected Profit/Loss: $${result.profit_loss.toFixed(2)}`;
    document.getElementById('result-plot').src = `data:image/png;base64,${result.plot_url}`;
    document.getElementById('result').style.display = 'block';
}

function displayError(message) {
    document.getElementById('error-message').innerText = message;
    document.getElementById('error-message').style.display = 'block';
}

function clearResult() {
    // Clear result and error messages
    document.getElementById('result').style.display = 'none';
    document.getElementById('error-message').style.display = 'none';
}

function clearForm() {
    // Clear form fields without resetting to default values
    document.getElementById('symbol').value = '';
    document.getElementById('forecast-period').selectedIndex = 0;
    document.getElementById('historical-years').value = '';
}
