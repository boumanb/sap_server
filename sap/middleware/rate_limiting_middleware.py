import json
import time

from decouple import config
from django.core.cache import cache
from django.http import HttpResponse

from sap.models import Student


class RateLimitingMiddleware(object):
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
        if cache.get(student.id) is None:
            bucket = {
                "tokens": self.max_amount - 1,
                "last_update": time.time()
            }
            cache.set(student.id, json.dumps(bucket))
        else:
            bucket = cache.get(student.id)
            reduced_bucket = self.reduce(bucket, tokens=1)
            if reduced_bucket is False:
                return HttpResponse("Too many requests", status=429, reason='Too many requests')
            else:
                cache.set(student.id, json.dumps(reduced_bucket))

    def refill_count(self, bucket):
        return int(((time.time() - bucket['last_update']) / self.refill_time))

    def reduce(self, bucket, **kwargs):
        bucket = json.loads(bucket)
        tokens = kwargs.get('tokens', 1)
        refill_count = self.refill_count(bucket)
        if (bucket['tokens'] + (refill_count * self.refill_amount)) > self.max_amount:
            bucket['tokens'] = self.max_amount
        else:
            bucket['tokens'] += refill_count * self.refill_amount
        bucket['last_update'] += refill_count * self.refill_time

        if tokens > bucket['tokens']:
            return False

        bucket['tokens'] -= tokens
        return bucket
