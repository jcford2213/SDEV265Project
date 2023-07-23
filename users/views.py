# from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
# from django.contrib.auth import authenticate, login
from .models import User
from .serializers import UserSerializer

# Performs CRUD operations on User model based on http request method


# Signing up new user
# Returns object username: String, tracked_stocks: List[]
@api_view(['POST'])
def signup_user(request):
    try:
      serializer = UserSerializer(data=request.data)
      if serializer.is_valid():
          serializer.save()
          print(serializer.data['id'])
      else:
         raise Exception
      return Response({'id': serializer.data['id'], 'username': serializer.data['username'], 'tracked_stocks': serializer.data['tracked_stocks']}, status=201)
    except Exception as e:
        print('Error: ', e)
        return Response({'error': f'An account with username {request.data["username"]} and or {request.data["email"]} already exists.'}, status=401)
      

# Logging in existing user
# Returning object userName: String, tracked_stocks: List
@api_view(['POST'])
def login_user(request):
    # Get http request data
    username = request.data['username']
    password = request.data['password']
    print(username, ' ', password)
    # Compare http request arguments with database user
    try:
      # get user based on http request data. Will raise exception if either doesn't match
      user = User.objects.get(username=username, password=password)
      if user.username == username and user.password == password:
        tracked_stocks = User.objects.values('tracked_stocks').get(username=username)
        return Response({'id': user.id, 'username': user.username, 'tracked_stocks': tracked_stocks}, status=201)
      else:
          raise Exception()
      
    except Exception as e:
        print('Error: ', e)
        return Response('username or password incorrect', status=401)
    
@api_view(['PATCH'])
def add_stock(request):
    try:
        user = User.objects.get(id=request.data.id)

      # split tracked stocks into a list of symbols
        tracked_stocks_list = user.tracked_stocks.split(',')
        tracked_stocks_list.append(request.data.stock)

        tracked_stocks_csv = ','.join(tracked_stocks_list)

        serializer = UserSerializer(user, data={'tracked_stocks': tracked_stocks_csv}, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(f'{request.data.stock} successfully added', status=201)
        else:
            raise Exception
    except Exception as e:
        print(e)
        return Response('Error adding a new stock to user table', status=401)
    
@api_view(['PATCH'])
def remove_stock(request):
    try:
        user = User.objects.get(id=request.data.id)

      # split tracked stocks into a list of symbols
        tracked_stocks_list = user.tracked_stocks.split(',')

        if request.data.stock in tracked_stocks_list: 
          tracked_stocks_list.remove(request.data.stock)
          tracked_stocks_csv = ','.join(tracked_stocks_list)
          serializer = UserSerializer(user, data={'tracked_stocks': tracked_stocks_csv}, partial=True)
        else:
          raise Exception

        if serializer.is_valid():
            serializer.save()
            return Response(f'{request.data.stock} successfully removed', status=201)
        else:
            raise Exception
    except Exception as e:
        print(e)
        return Response('Error removing a stock to user table', status=401)