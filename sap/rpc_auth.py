from sap.models import Student


def authenticate_by_token(request):
    token = request.META.get("HTTP_AUTHORIZATION")
    if token is None:
        return False

    student = Student.get_by_apitoken(token)
    if not student or student.check_token_valid() is False:
        return False
    else:
        return True

