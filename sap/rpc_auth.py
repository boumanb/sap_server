from sap.models import Student


def authenticate_by_token(request):
    token = request.META.get("HTTP_AUTHORIZATION")
    if token is None:
        return False

    q = Student.objects.filter(api_token=token)
    if not q:
        return False
    else:
        student = q[0]
        if student.check_token_valid():
            return True
        else:
            return False

