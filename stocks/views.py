# Listen for POST request containing stock ticker

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .utils.yfinaceConnection import getStockData
from .utils.timeSeriesAnalysisModels import getArModel, getMaModel, getArmaModel
from .utils.plotModelResults import plot_model_weekly, plot_model_monthly


@api_view(['POST'])
def returnTickerData(request):
    if request.method == 'POST':
        
        # Check for existing ticker from client
        if not request.data['ticker']:
            return Response({'error': 'Ticker not provided'}, status=400)
        
        # Attempt to access ticker from yfinance
        try:
          #  Get all information from yFianance ticker
          stockData = getStockData(request.data['ticker'])

          # Use ticker closePrices to generate time seriens Models
          arModel = getArModel(stockData['closePricesWeek'], stockData['closePricesMonth'])
          maModel = getMaModel(stockData['closePricesWeek'], stockData['closePricesMonth'])
          armaModel = getArmaModel(stockData['closePricesWeek'], stockData['closePricesMonth'])

          # Generate matplotlib graphs for each model and each timeframe
          arWeeklyImage = plot_model_weekly(arModel['fitted_values_weekly'], stockData['closePricesWeek'], 'AR Weekly')
          arMonthlyImage = plot_model_monthly(arModel['fitted_values_monthly'], stockData['closePricesMonth'], 'AR Monthly')

          maWeeklyImage = plot_model_weekly(maModel['fitted_values_weekly'], stockData['closePricesWeek'], 'MA Weekly')
          maMonthlyImage = plot_model_monthly(maModel['fitted_values_monthly'], stockData['closePricesMonth'], 'MA Monthly')

          armaWeeklyImage = plot_model_weekly(armaModel['fitted_values_weekly'], stockData['closePricesWeek'], 'ARMA Weekly')
          armaMonthlyImage = plot_model_monthly(armaModel['fitted_values_monthly'], stockData['closePricesMonth'], 'ARMA Monthly')
          
        except Exception as error:
          #  Sends an error message to client. args[0]is where the message value is stored
           return Response({'error': error.args[0]}, status=500)
        
        else:
          # Sends successful response with correct payload to client
          return Response(
            {
              'stockData': stockData['stockInfo'],
              'weeklyModel': {
                'ar': arWeeklyImage,
                'ma': maWeeklyImage,
                'arma': armaWeeklyImage
              },
              'monthlyModel': {
                'ar' : arMonthlyImage,
                'ma': maMonthlyImage,
                'arma': armaMonthlyImage
              }
            },
            status=200
          )
        
    return Response({'error': 'Invalid request method'}, status=405)
