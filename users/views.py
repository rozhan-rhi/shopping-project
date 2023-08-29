from rest_framework.views import APIView
from rest_framework.request import Request
from users.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .utils.token import Token
import datetime
from rest_framework import status
from users.models import User
from users.utils.sms import MessageSending
from users.utils.send_otp import SendOtp
from users.utils.validators import Validations
from django.contrib.auth.hashers import make_password
from users.utils.validators import Validations
import re
import os
from users.utils.redisService import Redis
redisObj=Redis()
validation=Validations()


class RegisterView(APIView):
     def post(self,request:Request):
        phoneNumber = request.data["phone"]
        phone_pattern = re.compile(os.getenv("PHONE_REGEX"))

        if not phone_pattern.match(phoneNumber):
            return  Response({"message": "enter valid phone number"},status.HTTP_400_BAD_REQUEST)

        user=User.objects.filter(phone=phoneNumber).first()
        if user:
            return Response({"message": "this phone number exists"}, status.HTTP_406_NOT_ACCEPTABLE)

        otp_code = str(SendOtp.createOtp())
        MessageSending.sending(phoneNumber, 1, "کد فعالسازی", otp_code)
        redisObj.set_value(otp_code, phoneNumber)
        token= Token.generateToken(request.data)
        return Response({"message":"verify your phone number","token": token,"code":otp_code },status.HTTP_200_OK)


class Check_otp_register(APIView):
    def post(self,request:Request):
        data=request.data
        print(data)
        phone=redisObj.get_value(data['code'])
        if phone!=None:
            token=request.META.get('HTTP_AUTHORIZATION', '')
            if not token:
                raise AuthenticationFailed
            decoded_token=Token.decodeToken(token)

            if decoded_token["phone"] != phone:
                raise ValueError({"message":"phone number doesn't match.try again!"})

            if validation.emptyCheck(data):
                return Response({"message":"fill all fields"},status.HTTP_406_NOT_ACCEPTABLE)

            if  validation.check_password(data["password"]):
                return Response({"message":"password should be at least 8 characters"},status.HTTP_406_NOT_ACCEPTABLE)

            if validation.checkConfirm_and_pass(data["password"], data["confirmPassword"]):
                return Response({"message":"password and confirm password are not the same"},status.HTTP_406_NOT_ACCEPTABLE)


            data["phone"] = phone
            print(type(request.data))

            serializer=UserSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data,status.HTTP_200_OK)
            return Response(None,status.HTTP_400_BAD_REQUEST)

        return Response({"message":"code is incorrect or has been expired.try again!"})

class LoginView(APIView):
    def post(self,request:Request):
        phone=request.data['phone']
        password=request.data['password']
        # try:
        user=User.objects.filter(phone=phone).first()
        if user is None:
            raise AuthenticationFailed({"message":"user not found!"})
        elif user.is_active== False:
            raise AuthenticationFailed({"message":"user is not active"})

        print(user.password,password)
        if not user.check_password(password):
            raise AuthenticationFailed({"message":"password is wrong!"})

        payload={
            'id':user.id,
            'phone':phone,
            'iat':datetime.datetime.utcnow(),
            'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=5)
        }

        token=Token.generateToken(payload)

        return Response({"message":"ok","token":token},status.HTTP_200_OK)



class ForgetPassword(APIView):
    def post(self,request:Request):
        phoneNumber=request.data["phone"]
        user=User.objects.filter(phone=phoneNumber).first()
        if not user:
            return Response({"message":"user not found"},status.HTTP_404_NOT_FOUND)
        otp_code=SendOtp.createOtp()
        redisObj.set_value(otp_code,phoneNumber)
        MessageSending.sending(phoneNumber, 1, "کد تایید", otp_code)
        token=Token.generateToken({"phone":phoneNumber})
        return Response({"message":"کد تایید ارسال شد","token":token,"code":otp_code})


class ResetPassword(APIView):       #check otp code and new password is in a single page
    def post(self,request:Request):
        data = request.data
        phone = redisObj.get_value(data['code'])
        # return Response(phone)
        if phone != None:
            token = request.META.get('HTTP_AUTHORIZATION', '')
            if not token:
                raise AuthenticationFailed
            decoded_token = Token.decodeToken(token)

            if decoded_token["phone"] != phone:
                raise ValueError({"message": "phone number doesn't match.try again!"})



            if validation.emptyCheck(data):
                return Response({"message": "fill all fields"}, status.HTTP_406_NOT_ACCEPTABLE)

            if validation.check_password(data["password"]):
                return Response({"message": "password should be at least 8 characters"}, status.HTTP_406_NOT_ACCEPTABLE)

            if validation.checkConfirm_and_pass(data["password"], data["confirmPassword"]):
                return Response({"message": "password and confirm password are not the same"},
                                status.HTTP_406_NOT_ACCEPTABLE)

            data["phone"] = phone
            user=User.objects.get(phone=phone)
            user.password=make_password(data["password"])
            user.save()
            return Response({"message":"password has been changed"},status.HTTP_202_ACCEPTED)
        return Response({"message":"code is incorrect or has been expired.try again!"})


class UserView(APIView):
    def get(self,request:Request):
        token=request.META.get('HTTP_AUTHORIZATION', '')
        if not token:
            raise AuthenticationFailed("Unauthorized!")

        payload=Token.decodeToken(token)
        user=User.objects.get(id=payload['id'])
        print(user)
        serializer=UserSerializer(user)
        return Response({"message":serializer.data},status.HTTP_200_OK)

