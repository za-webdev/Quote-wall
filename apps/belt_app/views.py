# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from .models import User,Quote,Favorite
from django.contrib import messages


def index(request):

	return render(request,'belt_app/index.html')


def register(request):

	response=User.objects.register(

		request.POST['name'],
		request.POST['alias'],
		request.POST['email'],
		request.POST['password'],
		request.POST['conf_password'],
		request.POST['dob'],

			)
	print response
	if response['valid']:
		request.session['user_id']=response['user'].id
		return redirect('/success')

	else:
		for error_message in response['errors']:
			messages.add_message(request,messages.ERROR,error_message)
		return redirect('/')


def login(request):

	response=User.objects.login(

		request.POST['email'],
		request.POST['password']

			)
	print response
	if response['valid']:
		request.session['user_id']=response['user'].id
		return redirect('/success')

	else:
		for error_message in response['errors']:
			messages.add_message(request,messages.ERROR,error_message)
		return redirect('/')

def success(request):
	if 'user_id' not in request.session:
		return redirect('/')

	all_quotes = Quote.objects.all().order_by('-created_at')
	favorites = Favorite.objects.filter(user_id=request.session['user_id'])
	for fav in favorites:
		all_quotes = all_quotes.exclude(id=fav.quote.id)

	context ={

	'user':User.objects.get(id=request.session['user_id']),
	'all_quotes': all_quotes,
	'favorites':Favorite.objects.filter(user_id=request.session['user_id'])

		}


	return render(request,'belt_app/success.html',context)

def remove(request,id):

	Favorite.objects.filter(quote_id=id).delete()


	return redirect('/success')

def add_quote(request,id):

	check=Quote.objects.quotesCheck(
		request.POST['name'],
		request.POST['content'],
		request.session['user_id']
		)
	if type(check) is list:
		for error in check:
			messages.add_message(request,messages.ERROR,error)
	return redirect('/success')


def delete(request,id):

	Quote.objects.get(id=id).delete()

	return redirect('/success')

def add_to_list(request,id):
		

		quote = Quote.objects.get(id=id)
		user=User.objects.get(id=request.session['user_id'])
		favorite=Favorite.objects.create(user=user,quote=quote)
		return redirect('/success')

def user_info(request,id):

	context={
	'user':User.objects.get(id=id),
	'your_quotes':Quote.objects.filter(created_by_id=id),

		}

	return render(request,'belt_app/user_info.html',context)

	

def logout(request):

	request.session.clear()

	return redirect('/')



