# Listen for POST request containing stock ticker

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .utils.apiconnection import getStockData


@api_view(['POST'])
def returnTickerData(request):
    if request.method == 'POST':
        
        # Check for existing ticker from client
        if not request.data['ticker']:
            return Response({'error': 'Ticker not provided'}, status=400)
        
        # Attempt to access ticker from yfinance
        try:
          stockData = getStockData(request.data['ticker'])
          
        except Exception as error:
          #  Sends an error message to client. args[0]is where the message value is stored
           return Response({'error': error.args[0]}, status=500)
        
        else:
          return Response(stockData, status=200)
        
    return Response({'error': 'Invalid request method'}, status=405)
