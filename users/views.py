from django.shortcuts import render, redirect
from django.contrib import messages
from sap.models import Teacher
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from .tokens import teacher_signup_token
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, TeacherRegisterForm, UserUpdateForm, TeacherUpdateForm
from rest_framework.authtoken.models import Token


def register(request):
    if request.method == "POST":
        u_form = UserRegisterForm(request.POST)
        t_form = TeacherRegisterForm(request.POST)
        if u_form.is_valid() and t_form.is_valid():
            t_mail = t_form.cleaned_data['email']
            try:
                teacher = Teacher.objects.get(email=t_mail)
            except Teacher.DoesNotExist:
                messages.error(request, f'email does not exist in the system, contact the system admin')
                return redirect("teacherportal-home")
            else:
                user = u_form.save(commit=False)
                user.is_active = False
                user.save()
                teacher.user = user
                teacher.save()
                current_site = get_current_site(request)
                message = render_to_string('users/teacher_activation_mail.html',
                                           {'user': user,
                                            'domain': current_site.domain,
                                            'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                                            'token': teacher_signup_token.make_token(user),
                                            })
                mail_subject = 'Activate teacher account'
                to_email = teacher.email
                email = EmailMessage(mail_subject, message, to=[[to_email]])
                email.send()
                messages.success(request, f'Account is successfully created, check your email to activate it.')
                return redirect('login')
    else:
        form = UserRegisterForm()
        form_teacher = TeacherRegisterForm()
        return render(request, 'users/register.html', {'form': form, 'form_teacher': form_teacher})
    form = UserRegisterForm(request.POST)
    form_teacher = TeacherRegisterForm(request.POST)
    return render(request, 'users/register.html', {'form': form, 'form_teacher': form_teacher})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and teacher_signup_token.check_token(user, token):
        user.is_active = True
        user.save()
        Token.objects.create(user=user)
        messages.success(request, f'{user.teacher.name} is successfully activated you can login now!')
        return redirect('login')
    else:
        messages.error(request, f'Activation link is invalid!')
        return redirect('login')


@login_required
def teacher(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        t_form = TeacherUpdateForm(request.POST, instance=request.user.teacher)
        if u_form.is_valid() and t_form.is_valid():
            u_form.save()
            t_form.save()
            messages.success(request, f'Your account has been updated')
            return redirect('teacher')
    else:
        u_form = UserUpdateForm(instance=request.user)
        t_form = TeacherUpdateForm(instance=request.user.teacher)

    context = {
        'u_form': u_form,
        't_form': t_form,
    }
    return render(request, 'users/teacher.html', context)


@login_required
def teacher_edit(request):
    u_form = UserUpdateForm(instance=request.user)
    t_form = TeacherUpdateForm(instance=request.user.teacher)
    context = {
        'u_form': u_form,
        't_form': t_form,
    }
    return render(request, 'users/teacher_edit.html', context)
