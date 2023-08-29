import math, random

class SendOtp:
    @staticmethod
    def createOtp():
        digits = "0123456789"
        otp = ""
        for i in range(5):
            otp += digits[math.floor(random.random() * 10)]

        return otp