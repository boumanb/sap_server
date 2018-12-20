import datetime
import secrets
import logging

from django.core import exceptions
from django.utils import timezone
from modernrpc.auth import set_authentication_predicate
from modernrpc.core import rpc_method
from modernrpc.core import REQUEST_KEY


from sap.models import Device, Student, Room, Attendance
from sap.rpc_auth import authenticate_by_token

logger = logging.getLogger('api')

@rpc_method
def echo(text):
    """
    Echoes the sent in string. For testing purpose.
    :param text: string containing text.
    :return: the sent in string.
    """

    return text


@rpc_method
@set_authentication_predicate(authenticate_by_token)
def echo_with_auth(text):
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
    if not q:
        r = {
            "success": False,
            "msg": "no device found"
        }
        return r

    device_id = q[0].id
    q = Student.objects.filter(device=device_id)
    if not q:
        r = {
            "success": False,
            "msg": "no student found for device"
        }
        return r

    student = q[0]
    if not student.device.is_confirmed():
        r = {
            "success": False,
            "msg": "device not confirmed"
        }
        return r

    token = secrets.token_urlsafe()
    token_valid_till = timezone.now() + datetime.timedelta(minutes=10)

    student.api_token = token
    student.api_token_valid_till = token_valid_till
    student.save()

    r = {
        "success": True,
        "token": token,
        "valid_till": token_valid_till
    }

    return r


@rpc_method
def mail_register_digits(student_nr, installation_uid):
    """
    Generates and sends TOTP to student mail.
    :param installation_uid: installation id of Android app
    :param student_nr: student number
    :return: JSON object with success boolean
    """
    q = Student.objects.filter(student_nr=student_nr)
    if not q:
        r = {
            "success": False
        }
        return r
    else:
        student = q[0]
        success = student.send_registration_mail(installation_uid)
        r = {
            "success": success
        }
        return r


@rpc_method
def confirm_register_digits(student_nr, register_digits, installation_uid):
    """
    Confirms registration of device using the student number and time base one time password
    :param register_digits: random generated digits
    :param student_nr: student number
    :param installation_uid: installation_uid from the app
    :return: JSON object with success boolean and installation id of the registered device
    """
    q = Student.objects.filter(student_nr=student_nr)
    if not q:
        r = {
            "success": False,
            "msg": "no student found"
        }
        return r
    else:
        student = q[0]
        if student.verify_registration(register_digits, installation_uid):
            r = {
                "success": True
            }
            return r
        else:
            r = {
                "success": False
            }
            return r


@rpc_method
def card_check(card_uid, reader_uid):
    """
    Creates attendance table entry and marks card check to true
    :param card_uid: the uid of card
    :param reader_uid: the uid of the reader used.
    :return: OK/NOK
    """
    student = Student.objects.get(card_uid=card_uid)
    room = Room.objects.get(reader_UID=reader_uid)

    college = room.find_college()

    try:
        college = room.find_college()

    except exceptions.ObjectDoesNotExist:
        r = {
            "success": False,
            "msg": "no college found"
        }
        return r

    else:
        student.attend_card(college)
        r = {
            "success": True
        }
        return r


@rpc_method
def phone_check(installation_uid, **kwargs):
    """
    Checks if the the attendance hits timewindow
    :param installation_uid: the installation_uid of the device
    :return: OK/NOK
    """
    device = Device.objects.get(installation_uid=installation_uid)
    student = Student.objects.get(device=device)
    request = kwargs.get(REQUEST_KEY)
    try:
        ip_add = request.META.get('HTTP_X_FORWARDED_FOR')
    except:
        ip_add = request.META.get('REMOTE_ADDR')

    logger.info("%s phone_check uid:%s ", ip_add, installation_uid)

    try:

        att = Attendance.objects.get(
            student=student,
            timestamp__gte=timezone.now() - datetime.timedelta(seconds=5))

    except exceptions.ObjectDoesNotExist:
        r = {
            "success": False,
            "msg": "too slow"
        }

        return r

    else:
        att.attend_phone()
        r = {
            "success": True,
            "msg": "attendance marked"
        }
        return r
