import jwt,datetime
from django.urls import path
from dotenv import load_dotenv
import os
load_dotenv()
from django.http import HttpResponseNotFound,HttpResponseForbidden

class CheckJwtMiddleware:
    # def __init__(self,get_response) :
        # self.get_response=get_response
        
    # def __call__(self,request):
        # sign_key = os.getenv("SECRET_JWT")
        # print(sign_key)
        # try :
        #     token = request.META.get('HTTP_AUTHORIZATION', '')
        #     if not token:
        #         return HttpResponseNotFound('user not found')
            
        #     try:
        #         payload = jwt.decode(token,sign_key, algorithms=["HS256"])
        #         print(payload)
        #         request.decoded=payload
        #     except:
        #         return HttpResponseForbidden('token expired!')
            
        #     response=self.get_response(request)
        #     return response
        # except Exception as e:
        #     print(e)
        #     return HttpResponseForbidden('token expired!')
        
    def process_view(self,request,view_func,view_args, view_kwargs):
        if request.path.startswith("/cart/"):
            sign_key = os.getenv("SECRET_JWT")
            print(sign_key)
            try :
                token = request.META.get('HTTP_AUTHORIZATION', '')
                if not token:
                    return HttpResponseNotFound('user not found')
                
                try:
                    payload = jwt.decode(token,sign_key, algorithms=["HS256"])
                    print(payload)
                    request.decoded=payload
                except:
                    return HttpResponseForbidden('token expired!')
                
                response=self.get_response(request)
                return response
            except Exception as e:
                print(e)
                return HttpResponseForbidden('token expired!')
        
        
             
def custom_middleware_decorator(view_func):
    def wrapper(request):
        CheckJwtMiddleware
        # Code to be executed before the view is called
        response = view_func(request)
        # Code to be executed after the view is called
        return response
    return wrapper