import ghasedakpack
import os
from rest_framework import exceptions
class MessageSending:
    @staticmethod
    def sending(receptor,type,template,param1):
        API_KEY = os.getenv("API_KEY")

        try:
            payload = {
                'receptor': receptor,
                "type": str(type),  # 1:sms   2:voice
                "template": template,
                'param1': param1
            }


            sms = ghasedakpack.Ghasedak(API_KEY)
            sms.verification(payload)

        except:
            raise exceptions.ValidationError