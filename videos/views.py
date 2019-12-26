from django.shortcuts import render 
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import UserForm, UserLoginForm, VideoForm
from django.urls import reverse
from django.contrib.auth import logout as auth_logout,authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
import json
# from django import forms
# from django.core.exceptions import ValidationError
# Create your views here.
def index(request):
	usfo=UserForm()
	return render(request,'videos/index.html',{'usfo':usfo})

def login(request):
	usfo=UserLoginForm(request.POST or None)
	err=None
	if request.method=='POST':
		if usfo.is_valid():
			email=usfo.cleaned_data.get('email')
			password=usfo.cleaned_data.get('password')
			user=authenticate(email=email,password=password)
			if user==None:
				# raise forms.ValidationError({'bark_volume': ["Must be louder!",]})
				err="Invalid login credentials"
			if user:
				if user.is_active:
					auth_login(request,user,backend='videos.backend.NewBackend')
					print(request.user.name,request.user.email)
					return HttpResponseRedirect(reverse('main_page'))
				else:
					return HttpResponse("Your account is inactive.")
	return render(request,'videos/login.html',{'usfo':usfo,'err':err})

def signup(request):
	usfo=UserForm(request.POST or None)
	if request.method == 'POST':
		print(usfo.is_valid(),usfo.clean_email(),usfo.clean_password2())
		print(usfo.clean())
		print(usfo.data)
		print(usfo.cleaned_data)
		if usfo.is_valid() and usfo.clean_email() and usfo.clean_password2():
			
			
			us=usfo.save(commit=False)
			print(usfo)
			us.set_password(usfo.clean_password2())
			us.save()
			auth_login(request,us,backend='videos.backend.NewBackend')
			return HttpResponseRedirect(reverse('main_page'))
		else:
			print(usfo.errors)

	return render(request,'videos/signup.html',{'usfo':usfo})

@login_required
def main_page(request):
	if request.method == 'POST':
		vform=VideoForm(request.POST,request.FILES)
		if vform.is_valid():
			vform.save()
			return HttpResponseRedirect(reverse('done'))
	else:
		vform=VideoForm()
	return render(request,'videos/form.html',{'vform':vform})



@login_required
def video_list(request):
	return render(request,'videos/video-list.html')


def logout(request):
	auth_logout(request)
	return HttpResponseRedirect(reverse('index'))



# import random
# def fun():
# 	a='4'
# 	while(a=='4'):
# 		print(random.choice(['a','b','c','d','e','f','g','h'])+random.choice(['1','2','3','4','5','6','7','8']))
# 		a=input()