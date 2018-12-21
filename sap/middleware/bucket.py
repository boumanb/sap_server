import json
import time

from decouple import config
from django.conf import settings
from django.core.cache import cache


class Bucket(object):
    student_id = 0
    tokens = 0
    last_update = 0

    if settings.TEST is True:
        max_amount = config('RL_TOKEN_MAX_AMOUNT', default=1000, cast=int)
        refill_time = config('RL_TOKEN_REFILL_TIME', default=1, cast=int)
        refill_amount = config('RL_TOKEN_REFILL_AMOUNT', default=1000, cast=int)
    else:
        max_amount = config('RL_TOKEN_MAX_AMOUNT', default=10, cast=int)
        refill_time = config('RL_TOKEN_REFILL_TIME', default=10, cast=int)
        refill_amount = config('RL_TOKEN_REFILL_AMOUNT', default=1, cast=int)

    def __init__(self, student_id):
        self.student_id = student_id
        bucket = cache.get(student_id)
        if cache.get(student_id) is None:
            bucket = {
                "tokens": self.max_amount - 1,
                "last_update": time.time()
            }
            cache.set(student_id, json.dumps(bucket))
        else:
            bucket = json.loads(bucket)
            self.tokens = bucket['tokens']
            self.last_update = bucket['last_update']

    def __refill_count(self):
        return int(((time.time() - self.last_update) / self.refill_time))

    def reduce(self, **kwargs):
        reduce_amount = kwargs.get('tokens', 1)
        refill_count = self.__refill_count()
        if (self.tokens + (refill_count * self.refill_amount)) > self.max_amount:
            self.tokens = self.max_amount
        else:
            self.tokens += refill_count * self.refill_amount
        self.last_update += refill_count * self.refill_time

        if reduce_amount > self.tokens:
            return False

        self.tokens -= reduce_amount
        return True

    def save(self):
        bucket = {
            "tokens": self.tokens,
            "last_update": self.last_update
        }
        cache.set(self.student_id, json.dumps(bucket))
