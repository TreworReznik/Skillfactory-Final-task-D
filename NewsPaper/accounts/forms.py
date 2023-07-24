from django.contrib.auth.models import Group
from allauth.account.forms import SignupForm
from django.core.mail import send_mail

class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        visitor = Group.objects.get(name='visitor')
        user.groups.add(visitor)
        send_mail(
            subject='Добро пожаловать !',
            message=f'{user.username}, вы успешно зарегистрировались!',
            from_email=None,  # будет использовано значение DEFAULT_FROM_EMAIL
            recipient_list=[user.email],)
        return user