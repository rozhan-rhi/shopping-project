import jwt
import functools
from django.urls import path
from dotenv import load_dotenv
import os
load_dotenv()
from django.http import HttpResponseNotFound,HttpResponseForbidden
from home.middleware.authMiddleware import CheckJwtMiddleware
from django.utils.decorators import wraps


def checkJwt_decorator(view_func):
    
    # sign_key = os.getenv("SECRET_JWT")
    @wraps(view_func)
    def wrapper(request,*args,**kwargs):
        CheckJwtMiddleware()
        # try :
        #     token = request.META.get('HTTP_AUTHORIZATION', '')
        #     print(token)
        #     if not token:
        #         return HttpResponseNotFound('user not found')
            
        #     try:
        #         payload = jwt.decode(token,sign_key, algorithms=["HS256"])
        #         print(payload)
        #         request.decoded=payload
        #         return view_func(request, *args, **kwargs)
        #     except:
        #         return HttpResponseForbidden('token expired!')
            
        # except Exception as e:
        #     print(e)
        #     return HttpResponseForbidden('token expired!')
    return wrapper

        
        
        
