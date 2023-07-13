from django.contrib.auth.models import Group
from allauth.account.forms import SignupForm


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        visitor = Group.objects.get(name='visitor')
        user.groups.add(visitor)
        return user