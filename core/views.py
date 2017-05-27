# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import Context, Template
from models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
def home(request):
	if request.user.is_authenticated():
		return redirect(account)
	else:
		return redirect(login)

def login(request):
	context = {}
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			if user.is_staff:
				auth_login(request, user)
				return redirect(home)
			else:
				return HttpResponse("<center>User is inactive contact admin.</center>")
		else:
			return HttpResponse("<center>Invalid Credentials <a href='/login'>Back</a></center>")
	return render(request, 'login.html', context) 

def signup(request):
	if request.method == "POST":
		name = request.POST.get('name')
		username = request.POST.get('username')
		email = request.POST.get('email')
		password = request.POST.get('password')
		dob = request.POST.get('dob')
		try:
			usr = User.objects.get(email = email)
			return HttpResponse("<center>User Already exist</center>")
		except ObjectDoesNotExist:
			obj = User.objects.create_user(first_name= name ,username = username, email = email, password = password)
			profile = Profile.objects.get_or_create(user = obj,birth_date=dob)
			return HttpResponse("<center>Registration succesful, Click <a href='/login/'>here</a> to login in!<center>")
			
	context = {}
	return render(request, 'signup.html', context) 


def account(request):
	try:
		User = request.user
		profile,created = Profile.objects.get_or_create(user=User)
		if request.method == "POST":
			User.first_name = request.POST.get('name')
			User.email = request.POST.get('email')
			profile.city = request.POST.get('city')
			profile.country = request.POST.get('country')
			profile.save()
			User.save()
		context = {'Profile': profile}
	except ObjectDoesNotExist:
		context = {}
	return render(request, 'account.html', context) 

def logout(request):
	auth_logout(request);
	return redirect(login)

