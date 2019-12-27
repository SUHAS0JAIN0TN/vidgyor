from django.shortcuts import render 
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import UserForm, UserLoginForm, VideoForm,filter_form
from django.urls import reverse
from django.contrib.auth import logout as auth_logout,authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
import json
from .models import vid
from django.core.paginator import Paginator
# from django import forms
# from django.core.exceptions import ValidationError
# Create your views here.
def index(request):
	usfo=UserForm()
	return render(request,'videos/index.html',{'usfo':usfo})

def login(request):
	usfo=UserLoginForm(request.POST or None)
	# err=None
	if request.method=='POST':
		if usfo.is_valid():
			email=usfo.cleaned_data.get('email')
			password=usfo.cleaned_data.get('password')
			user=authenticate(email=email,password=password)
			# if user==None:
				# raise forms.ValidationError({'bark_volume': ["Must be louder!",]})
				# err="Invalid login credentials"
			if user:
				if user.is_active:
					auth_login(request,user,backend='videos.backend.NewBackend')
					print(request.user.name,request.user.email)
					return HttpResponseRedirect(reverse('video_list'))
				else:
					return HttpResponse("Your account is inactive.")
	return render(request,'videos/login.html',{'usfo':usfo,})

def signup(request):
	usfo=UserForm(request.POST or None)
	if request.method == 'POST':
		if usfo.is_valid() and usfo.clean_email() and usfo.clean_password2():
			
			
			us=usfo.save(commit=False)
			us.set_password(usfo.clean_password2())
			us.save()
			auth_login(request,us,backend='videos.backend.NewBackend')
			return HttpResponseRedirect(reverse('video_list'))
		else:
			print(usfo.errors)

	return render(request,'videos/signup.html',{'usfo':usfo})

@login_required
def add_form(request):
	if request.method == 'POST':
		vform=VideoForm(request.POST,request.FILES)
		if vform.is_valid():
			vform.save()
			return HttpResponseRedirect(reverse('video_list'))
	else:
		vform=VideoForm()
	return render(request,'videos/form.html',{'vform':vform})


@login_required
def edit_form(request,id):
	v=vid.objects.get(id=id)
	# if request.method == 'GET':
	vform=VideoForm(request.POST or None,request.FILES or None,instance=v)
	# print(vform.id)
	# vform=VideoForm(instance=v)
	if request.method == 'POST':
		if vform.is_valid():
			vform.save()
			return HttpResponseRedirect(reverse('video_list'))
	return render(request,'videos/form.html',{'vform':vform})



@login_required
def video_list(request):
	filterForm=filter_form(request.POST or None)
	if(request.method=="POST"):
		filterForm=filter_form(request.POST)
		request.session['form']=request.POST
	elif(request.session.get('form',None)):
		filterForm=filter_form(request.session['form'])
	else:
		filterForm=filter_form(None)
	print(filterForm.data.get('name'))
	# print(filterForm.name,filterForm.from_date,filterForm.to_date)
	data_list=vid.objects.all()
	if(filterForm.data.get('name',None)):
		data_list=data_list.filter(title__contains=filterForm.data['name'])
	if(filterForm.data.get('from_date',None)):
		data_list=data_list.filter(date__gte=filterForm.data['from_date'])
	if(filterForm.data.get('to_date',None)):
		data_list=data_list.filter(date__lte=filterForm.data['to_date'])
	paginator = Paginator(data_list, 2)
	page = request.GET.get('page')
	data = paginator.get_page(page)
	print(data)
	print(request.session.get('form',None))
	return render(request,'videos/video-list.html',{'data':data,'filterForm':filterForm})

@login_required
def delete(request,id):
	vid.objects.get(id=id).delete()
	return HttpResponseRedirect(reverse('video_list'))


def logout(request):
	auth_logout(request)
	return HttpResponseRedirect(reverse('index'))



# import random
# def fun():
# 	a='4'
# 	while(a=='4'):
# 		print(random.choice(['a','b','c','d','e','f','g','h'])+random.choice(['1','2','3','4','5','6','7','8']))
# 		a=input()