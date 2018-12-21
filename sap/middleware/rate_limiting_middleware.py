import json

from decouple import config
from django.conf import settings
from django.http import HttpResponse

from sap.middleware.bucket import Bucket
from sap.models import Student


class RateLimitingMiddleware(object):
    if settings.TEST is True:
        max_amount = config('RL_TOKEN_MAX_AMOUNT', default=1000, cast=int)
        refill_time = config('RL_TOKEN_REFILL_TIME', default=1, cast=int)
        refill_amount = config('RL_TOKEN_REFILL_AMOUNT', default=1000, cast=int)
        excluded_methods = config('RL_EXCLUDED_RPC_METHODS', default='login')
    else:
        max_amount = config('RL_TOKEN_MAX_AMOUNT', default=10, cast=int)
        refill_time = config('RL_TOKEN_REFILL_TIME', default=10, cast=int)
        refill_amount = config('RL_TOKEN_REFILL_AMOUNT', default=1, cast=int)
        excluded_methods = config('RL_EXCLUDED_RPC_METHODS', default='login')

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.process_request(request)
        if response is None:
            return self.get_response(request)
        return response

    def process_request(self, request):
        if not request.path.startswith('/rpc/'):
            return None
        if json.loads(request.body)['method'] in self.excluded_methods:
            return None
        student = Student.get_by_apitoken(request.META.get("HTTP_AUTHORIZATION"))
        bucket = Bucket(student.id)
        if bucket.reduce(tokens=1) is False:
            return HttpResponse("Too many requests", status=429, reason='Too many requests')
        else:
            bucket.save()

