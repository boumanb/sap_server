from django.conf import settings
from rest_framework.authtoken.models import Token


def global_settings(request):
    return {
        'BASE_URL_W_TRAILING_SLASH': settings.BASE_URL_W_TRAILING_SLASH,
        'BASE_URL': settings.BASE_URL_W_TRAILING_SLASH[:-1],
        'API_URL': settings.BASE_URL_W_TRAILING_SLASH + 'api/'
    }


def api_token(request):
    if request.user.is_authenticated:
        token = Token.objects.get(user=request.user)
        return {
            'API_TOKEN': token
        }
    else:
        return {
            'API_TOKEN': ''
        }

