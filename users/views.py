import jwt
import datetime

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from rest_framework.exceptions import AuthenticationFailed


from django.contrib.auth import authenticate

from .models import CustomUser
from .serializers import UserSerializer, TokenObtainPairSerializer
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def user_registration(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "User successfully registered."})
        return Response(serializer.errors, status=400)




@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def user_login(request):
    if request.method == 'POST':
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')
        
        user = authenticate(phone_number=phone_number, password=password)
        if user is None:
            raise AuthenticationFailed("User not found")

        # Generate access token
        access_token = AccessToken.for_user(user)

        # Generate refresh token
        refresh_token = RefreshToken.for_user(user)

        # Set token expiry time
        access_token_lifetime = datetime.timedelta(minutes=5)
        refresh_token_lifetime = datetime.timedelta(days=1)

        # Set token expiration time in payload
        access_token['exp'] = datetime.datetime.utcnow() + access_token_lifetime
        refresh_token['exp'] = datetime.datetime.utcnow() + refresh_token_lifetime

        # Set the tokens in the response cookies
        response = Response()
        response.set_cookie(key='jwt', value=str(access_token), httponly=True)
        response.set_cookie(key='refresh_token', value=str(refresh_token), httponly=True)

        response.data = {
            'jwt': str(access_token),
            'refresh_token': str(refresh_token),
            'email':str(user.email)
        }

        return response
        

@api_view(['POST'])
def user_logout(request):
    response =Response()
    response.delete_cookie('jwt')
    response.data  ={
        'message':'logout successfully'
    }
    return response


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def refresh_token(request):
    refresh_token = request.data.get('refresh_token')
    
    try:
        # Decode the refresh token
        refresh_token = RefreshToken(refresh_token)
        # Create a new access token
        access_token = AccessToken.for_user(refresh_token.user)
        access_token_lifetime = datetime.timedelta(minutes=5)
        access_token['exp'] = datetime.datetime.utcnow() + access_token_lifetime


        response = Response()
        response.set_cookie(key='jwt', value=str(access_token), httponly=True)

        response.data = {
            'jwt': str(access_token),
        }

        return response
    except jwt.ExpiredSignatureError:
        return Response({'error': 'Refresh token has expired'}, status=400)
    except jwt.InvalidTokenError:
        return Response({'error': 'Invalid refresh token'}, status=400)
    except Exception as e:
        return Response({'error': 'An error occurred during token refresh'}, status=400)


@api_view(['POST'])
def get_user_from_access_token(request):
    access_token = request.data.get('access_token')

    try:
        # Decode the access token
        access_token_instance = AccessToken(access_token)
        payload = access_token_instance.payload
        user_id = payload['user_id']

        # Get the user object from the database
        user = CustomUser.objects.get(id=user_id)

        # Serialize the user data and return the response
        serializer = UserSerializer(user)
        return Response(serializer.data)
    except jwt.ExpiredSignatureError:
        return Response({'error': 'Access token has expired'}, status=400)
    except jwt.InvalidTokenError:
        return Response({'error': 'Invalid access token'}, status=400)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)
    except Exception as e:
        return Response({'error': 'Unauthorised Access'}, status=401)