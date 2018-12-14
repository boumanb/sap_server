import datetime
import secrets

from django.utils import timezone
from modernrpc.auth import set_authentication_predicate
from modernrpc.core import rpc_method


from sap.models import Device, Student, Room, Attendance
from sap.rpc_auth import authenticate_by_token



@rpc_method
# @set_authentication_predicate(authenticate_by_token)
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


@rpc_method
def mail_register_digits(student_nr, installation_uid):
    """
    Generates and sends TOTP to student mail.
    :param installation_uid: installation id of Android app
    :param student_nr: student number
    :return: JSON object with success boolean and installation id of the registered device
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
            "success": success,
            "installation_uid": installation_uid
        }
        return r


@rpc_method
def confirm_register_digits(student_nr, register_digits):
    """
    Confirms registration of device using the student number and time base one time password
    :param register_digits: random generated digits
    :param student_nr: student number
    :return: JSON object with success boolean and installation id of the registered device
    """

    q = Student.objects.filter(student_nr=student_nr)
    if not q:
        r = {
            "success": False
        }
        return r
    else:
        student = q[0]
        if student.verify_registration(register_digits):
            r = {
                "success": True,
                "installation_uid": student.device.installation_uid
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
    :param student_nr: the uid of the reader used.
    :return: OK/NOK
    """

    student = Student.objects.get(card_uid=card_uid)
    room = Room.objects.get(reader_UID=reader_uid)

    college = room.find_college()

    if not college:
        response = {
            "msg": "No class foo!"
        }
        return response
    else:
        student.attend_card(college)
        response = {
            "msg": "Ok"
        }
        return response

@rpc_method
def phone_check(uid):
    """
    Checks if the the attendance hits timewindow
    :param uid: the uid of the device
    :return: OK/NOK
    """
    device = Device.objects.get(installation_uid=uid)
    student = Student.objects.get(device=device)
    att = Attendance.objects.get(
        student=student,
        timestamp__gte=timezone.now() - datetime.timedelta(seconds=5))
    if not att:
        response = {
            "msg": "Too slow"
        }
        return response

    else:
        att.attend_phone()
        response = {
            "msg": "Attendance marked"
        }
        return response
