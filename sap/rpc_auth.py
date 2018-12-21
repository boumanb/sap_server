from sap.models import Student


def authenticate_by_token(request):
    token = request.META.get("HTTP_AUTHORIZATION")
    if token is None:
        return False

    student = Student.get_by_apitoken(token)
    if not student:
        return False
    else:
        if student.check_token_valid():
            return True
        else:
            return False

