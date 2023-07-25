# Listen for POST request containing stock ticker
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .utils.yfinaceConnection import getStockData
from .utils.timeSeriesAnalysisModels import getArModel, getMaModel, getArmaModel
from .utils.plotModelResults import plot_model_weekly, plot_model_monthly

from .models import TrackedStock
from .serializers import TrackedStockSerializer


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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_tracked_stocks(request):
    if request.method != 'GET':
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    try:
      tracked_stocks_model = TrackedStock.objects.get(user=request.user)
    except TrackedStock.DoesNotExist:
       return Response({'error': 'TrackedStock object not found for the current user.'}, status=status.HTTP_404_NOT_FOUND)
    
    # Serialize tracked_stocks_data in order to be returned over http
    serializer = TrackedStockSerializer(tracked_stocks_model)

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def add_tracked_stock(request):
    if request.method != 'PUT':
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    try:
      tracked_stocks_model = TrackedStock.objects.get(user=request.user)
      print(tracked_stocks_model.tracked_stocks, 'tracked stocks')
    except TrackedStock.DoesNotExist:
       return Response({'error': 'TrackedStock object not found for the current user.'}, status=status.HTTP_404_NOT_FOUND)
    
    new_ticker = request.data.get('tickerToAdd')

    # Check if tracked_stocks_model is empty
    if tracked_stocks_model.tracked_stocks != None:
       # Convert data into a list and append new ticker
      stocks_list = tracked_stocks_model.tracked_stocks.split(',')
      print(len(stocks_list))
      print(f'new_ticker is {new_ticker}')
      stocks_list.append(new_ticker)
      print(len(stocks_list))

      # Convert list with new ticker into a comma seperated string and save the model
      new_stocks_string = ','.join(stocks_list)
      tracked_stocks_model.tracked_stocks = new_stocks_string
    else:
      tracked_stocks_model.tracked_stocks = new_ticker

    # save the updated model
    tracked_stocks_model.save()
       

    # Serialize tracked_stocks_data in order to be returned over http
    serializer = TrackedStockSerializer(tracked_stocks_model)

    return Response(serializer.data, status=status.HTTP_200_OK)
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def delete_tracked_stock(request):
    if request.method != 'PUT':
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    try:
      tracked_stocks_model = TrackedStock.objects.get(user=request.user)
    except TrackedStock.DoesNotExist:
       return Response({'error': 'TrackedStock object not found for the current user.'}, status=status.HTTP_404_NOT_FOUND)
    
    # Convert data into a list and remove ticker
    stocks_list = tracked_stocks_model.tracked_stocks.split(',')
    ticker = request.data.get('tracked_stock')

    if ticker not in stocks_list:
        return Response({'error': 'Ticker is not found in TrackedStock object.'}, status=status.HTTP_404_NOT_FOUND)

    stocks_list.remove(ticker)

    # Convert list with new ticker into a comma seperated string and save the model
    new_stocks_string = ','.join(stocks_list)
    tracked_stocks_model.tracked_stocks = new_stocks_string
    tracked_stocks_model.save()

    # Serialize tracked_stocks_data in order to be returned over http
    serializer = TrackedStockSerializer(tracked_stocks_model)

    return Response(serializer.data, status=status.HTTP_200_OK)
    