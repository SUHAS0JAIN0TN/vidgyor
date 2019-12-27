from django import forms
from .models import User,vid
from django.contrib.auth import authenticate

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
        def clean_password(self):
                email = self.cleaned_data.get('email')
                password = self.cleaned_data.get('password')
                user=authenticate(email=email,password=password)
                if not user: 
                        raise forms.ValidationError("Wrong Credentials")
                return password

class VideoForm(forms.ModelForm):
        class Meta:
                model=vid
                fields='__all__'

        def clean_thumbnail(self):
                thumb =self.cleaned_data.get('thumbnail')
                print(thumb.name.split('.')[-1])
                if not (thumb.name.split('.')[-1]=='jpg' or thumb.name.split('.')[-1]=='png' or thumb.name.split('.')[-1]=='jpeg'):
                        raise forms.ValidationError("Thumbnail should be in jpg or jpeg or png format")
                return thumb

class filter_form(forms.Form):
        name=forms.CharField(required=False)
        from_date=forms.DateField(widget=forms.TextInput( {'placeholder':"Ex: 10/10/2010"}),required=False)
        to_date=forms.DateField(widget=forms.TextInput( {'placeholder':"Ex: 10/10/2010"}),required=False)