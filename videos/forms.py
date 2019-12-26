from django import forms
from .models import User,vid

class UserForm(forms.ModelForm):
        password1=forms.CharField(label='password',widget=forms.PasswordInput)
        password2=forms.CharField(label='confirm password',widget=forms.PasswordInput)

        class Meta:
                model=User
                fields=('email','name')

        def clean_email(self):
                email = self.cleaned_data.get('email')
                qs = User.objects.filter(email=email)
                if qs.exists():
                        raise forms.ValidationError("email is taken")
                return email

        def clean_password2(self):
                password1 = self.cleaned_data.get("password1")
                password2 = self.cleaned_data.get("password2")
                if password1 and password2 and password1 != password2:
                        raise forms.ValidationError("Passwords don't match")
                return password2

class UserLoginForm(forms.Form):
        email=forms.EmailField(label='Email')
        password=forms.CharField(label='password', widget=forms.PasswordInput)

        # def clean_email(self):
        #       email = self.cleaned_data.get('email')
        #       qs = User.objects.filter(email=email)
        #       if qs.exists():
        #               raise forms.ValidationError("email is taken")
        #       return email


class VideoForm(forms.ModelForm):
        class Meta:
                model=vid
                fields='__all__'