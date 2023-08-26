from django.test import TestCase

# Create your tests here.
from utils.redisService import Redis
redisObj=Redis()

redisObj.set_value("name","rozhan")
print(redisObj.get_value("age"))