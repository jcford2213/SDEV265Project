from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def returnTickerData(request):
    if request.method == 'POST':
        ticker = request.data.get('ticker')
        if not ticker:
            return Response({'error': 'Ticker not provided'}, status=400)
        stockData = getStockData(ticker)
        return Response(stockData)
    return Response({'error': 'Invalid request method'}, status=405)