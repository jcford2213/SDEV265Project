from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .serializer import UserSerializer
from stocks.models import TrackedStock

# from rest_framework.decorators import api_view

@api_view(['POST'])
@permission_classes([AllowAny])
def user_registration(request):
    if request.method != 'POST':
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # Get the data from the request
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    if not username or not password:
        return Response({'error': 'Both username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if username already exists
    if User.objects.filter(username=username).exists():
        return Response({'error': 'This username is already taken.'}, status=status.HTTP_409_CONFLICT)
    
    # Create the user and corresponding tracked stocks table
    try:
        user = User.objects.create_user(username=username, password=password, email=email)
        TrackedStock.objects.create(user=user)

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': 'An error occurred while creating the user.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    

@api_view(['GET'])
@permission_classes([AllowAny])
def get_user(request):
    if request.method != 'GET':
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # Get the user associated with the tokem
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)
    


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def user_logout(request):
#     if request.method != 'POST':
#         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

#     username = request.data.get('username')
#     password = request.data.get('password')
#     user = authenticate(username=username, password=password)
#     if not user:
#       return Response(status=status.HTTP_401_UNAUTHORIZED)
    
#     logout(request)
#     return Response({'message': 'Logout successful!'}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def user_deletion(request):
    if request.method != 'DELETE':
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    request.user.delete()
    return Response({'message': 'User deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)