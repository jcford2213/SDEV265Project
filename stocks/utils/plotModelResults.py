import matplotlib.pyplot as plt
import io
import base64

## Plot Weekl Model function
def plot_model_weekly(fitted_values_weekly, close_prices_week, model_name):
    figure = plt.figure()
    plt.plot(close_prices_week.index[:len(fitted_values_weekly)], close_prices_week[:len(fitted_values_weekly)], label='Close Prices (Weekly)')
    plt.plot(close_prices_week.index[:len(fitted_values_weekly)], fitted_values_weekly, label=model_name + ' Model (Weekly)')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.title('Close Prices - ' + model_name + ' Model')
    plt.legend()

    # Convert figure into JPEG image
    buffer = io.BytesIO()
    figure.savefig(buffer, format='jpeg')
    buffer.seek(0)

    # Encode the image data in base64
    imageData = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return imageData


## Plot montly model function
def plot_model_monthly(fitted_values_monthly, close_prices_month, model_name):
    figure = plt.figure()
    plt.plot(close_prices_month.index[:len(fitted_values_monthly)], fitted_values_monthly, label=model_name + ' Model (Monthly)')
    plt.plot(close_prices_month.index[:len(fitted_values_monthly)], close_prices_month[:len(fitted_values_monthly)], label='Close Prices (Monthly)')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.title('Close Prices - ' + model_name + ' Model')
    plt.legend()

    # Convert figure into JPEG image
    buffer = io.BytesIO()
    figure.savefig(buffer, format='jpeg')
    buffer.seek(0)

    # Encode the image data in base64
    imageData = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return imageData
