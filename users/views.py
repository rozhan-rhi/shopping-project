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
from users.utils.redisService import Redis
redisObj=Redis()



class RegisterView(APIView):
     def post(self,request:Request):
        phoneNumber = request.data["phone"]
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            otp_code = str(SendOtp.createOtp())

            MessageSending.sending(phoneNumber, 1, "کد فعالسازی", otp_code)

            redisObj.set_value(otp_code, phoneNumber)

            token= Token.generateToken(request.data)
            return Response({"message":"verify your phone number","token": token,"code":otp_code },status.HTTP_201_CREATED)
        return Response(None,status.HTTP_400_BAD_REQUEST)


class Check_otp_register(APIView):
    def post(self,request:Request):
        code=request.data['code']
        value=redisObj.get_value(code)
        # return Response(value)
        if value!=None:
            token=request.META.get('HTTP_AUTHORIZATION', '')
            if not token:
                raise AuthenticationFailed
            decoded_token=Token.decodeToken(token)

            if decoded_token["phone"] != value:
                raise ValueError("phone number doesn't match.try again later!")


            decoded_token["is_active"]=True
            user = User.objects.get(phone=decoded_token["phone"])
            serializer=UserSerializer(user,data=decoded_token)
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
        elif user.is_active== False:
            raise AuthenticationFailed("user is not active")

        print(user.password,password)
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



class ForgetPassword(APIView):
    def post(self,request:Request):
        phoneNumber=request.data["phone"]
        user=User.objects.get(phone=phoneNumber)
        if not user:
            return Response({"error":"user not found"},status.HTTP_404_NOT_FOUND)
        otp_code=SendOtp.createOtp()
        redisObj.set_value(otp_code,phoneNumber)
        MessageSending.sending(phoneNumber, 1, "کد تایید", otp_code)
        token=Token.generateToken({"phone":phoneNumber})
        return Response({"message":"کد تایید ارسال شد","token":token})


class ResetPassword(APIView):       #check otp code and new password is in a single page
    def post(self,request:Request):
        data = request.data
        value = redisObj.get_value(data['code'])

        if value==None:
            return Response({"error":"code is wrong"},status.HTTP_404_NOT_FOUND)

        if not data["token"]:
            raise AuthenticationFailed

        validation = Validations()
        validation.emptyCheck( data )
        validation.check_password(data["password"])
        validation.checkConfirm_and_pass(data["password"],data["confirmPassword"])

        user=User.objects.get(phone=data["phone"])
        user.password=make_password(data["password"])
        user.save()

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

