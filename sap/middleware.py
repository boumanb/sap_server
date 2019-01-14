import requests
from django.conf import settings
import logging

class ApiLog(object):
    def log(self, request):
        return 0