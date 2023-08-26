
from django.core.cache import cache
from django.conf import settings
settings.configure()
from django.core.cache.backends.base import DEFAULT_TIMEOUT

class Redis:
    def __init__(self):
        self.CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


    def set_value(self,key,value):

        cache.set(key, value, timeout=self.CACHE_TTL)

    def get_value(self,key):
        value=cache.get(key)
        if  value != None:
            return value

