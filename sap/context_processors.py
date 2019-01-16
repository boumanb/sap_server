from django.conf import settings


def global_settings(request):
    return {
        'BASE_URL_W_TRAILING_SLASH': settings.BASE_URL_W_TRAILING_SLASH,
        'BASE_URL': settings.BASE_URL_W_TRAILING_SLASH[:-1]
    }
