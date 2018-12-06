import datetime
from django.utils import timezone

from modernrpc.auth import set_authentication_predicate
from modernrpc.core import rpc_method

from sap.models import Device, Student
from sap.rpc_auth import authenticate_by_token
import secrets


@rpc_method
@set_authentication_predicate(authenticate_by_token)
def echo(text):
    """
    Echoes the sent in string. For testing purpose.
    :param text: string containing text.
    :return: the sent in string.
    """

    return text


@rpc_method
def login(installation_uid):
    """
    Returns a API token for further API usage
    :param installation_uid: installation UID of Android app
    :return: JSON containing token
    """

    q = Device.objects.filter(installation_uid=installation_uid)
    device_id = q[0].id

    token = secrets.token_urlsafe()
    token_valid_till = timezone.now() + datetime.timedelta(minutes=10)

    q = Student.objects.filter(device=device_id)
    student = q[0]

    student.api_token = token
    student.api_token_valid_till = token_valid_till
    student.save()

    r = {
        "token": token,
        "valid_till": token_valid_till
    }

    return r
