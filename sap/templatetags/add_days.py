import datetime

from django import template

register = template.Library()


@register.filter()
def add_days(days):
    newDate = datetime.date.today() + datetime.timedelta(days=days)
    return newDate
