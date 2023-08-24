from rest_framework.views import APIView
from rest_framework.request import Request
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from .utils import Token
import jwt,datetime
from rest_framework import status
from .models import User
import math, random
# from kavenegar import *
import ghasedakpack

from dotenv import load_dotenv
import os
load_dotenv()

CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


class RegisterView(APIView):
    def send_otp(self,receptor):
        API_KEY = os.getenv("API_KEY")
        digits = "0123456789"
        otp = ""
        for i in range(5):
            otp += digits[math.floor(random.random() * 10)]
        try:
            payload = {
                'receptor': receptor,
                "type": "1",  # 1:sms   2:voice
                "template": "قالب شماره  1",
                'param1': otp
            }

            sms = ghasedakpack.Ghasedak(API_KEY)
            sms.verification(payload)
            return otp

        except :
            return Response({"error": "e"})

    def post(self,request:Request):
        phoneNumber = request.data["phone"]
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            otp_code = str(self.send_otp(phoneNumber))
            cache.set(otp_code, phoneNumber  , timeout=CACHE_TTL)
            print('not from cache')
            token=Token.generateToken(request.data)
            return Response({"message":"verify your phone number","token": token,"code":otp_code },status.HTTP_201_CREATED)
        return Response(None,status.HTTP_400_BAD_REQUEST)


class Check_otp(APIView):
    def post(self,request:Request):
        code=request.data['code']
        value=cache.get(code)
        # return Response(value)
        if value!=None:
            token=request.META.get('HTTP_AUTHORIZATION', '')
            if not token:
                raise AuthenticationFailed
            decoded_token=Token.decodeToken(token)

            # if decoded_token.phone != value:
            #     raise ValueError("phone number doesn't match.try again later!")
            #
            #
            user = User.objects.get(phone=decoded_token["phone"])
            serializer=UserSerializer(user,data=decoded_token,is_active=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status.HTTP_200_OK)
            return Response(None,status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self,request:Request):
        phone=request.data['phone']
        password=request.data['password']
        # try:
        user=User.objects.filter(phone=phone).first()
        if user is None:
            raise AuthenticationFailed("user not found!")

        if not user.check_password(password):
            raise AuthenticationFailed("password is wrong!")

        payload={
            'id':user.id,
            'phone':phone,
            'iat':datetime.datetime.utcnow(),
            'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=5)
        }

        token=Token.generateToken(payload)

        return Response({"token":token},status.HTTP_200_OK)


class UserView(APIView):
    def get(self,request:Request):
        token=request.META.get('HTTP_AUTHORIZATION', '')
        if not token:
            raise AuthenticationFailed("Unauthorized!")

        payload=Token.decodeToken(token)
        user=User.objects.get(id=payload['id'])
        print(user)
        serializer=UserSerializer(user)
        return Response(serializer.data,status.HTTP_200_OK)

