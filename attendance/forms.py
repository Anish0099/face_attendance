from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    photo = forms.ImageField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'photo')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            user_profile = UserProfile(user=user, photo=self.cleaned_data['photo'])
            user_profile.save()
        return user
    

class AttendanceForm(forms.Form):
    photo = forms.ImageField(required=True)