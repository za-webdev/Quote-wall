# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
from datetime import datetime
import bcrypt


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9+-._]+@[a-zA-Z0-9+-._]+\.[a-zA-Z]+$')


class UserManager(models.Manager):
	def register(self,name,alias,email,password,conf_password,dob):

		response={
			'valid':True,
			'errors':[],
			'user':None
		}

		#for name
		if len(name)<1:
			response['errors'].append('First name is required')
		elif len(name)<2:
			response['errors'].append(' First Name must be greater than 2 characters or more')


		#for alias
		if len(alias)<1:
			response['errors'].append('Username is required')
		elif len(alias)<2:
			response['errors'].append('Username must be greater than 2 characters or more')
			#for email
		if len(email)<1:
			response['errors'].append('Email is required')
		elif not EMAIL_REGEX.match(email):
			response['errors'].append('Invalid Email')
		else:
			email_list=User.objects.filter(email=email.lower())
			if len (email_list)>0:
				response['errors'].append('Email already exist')

		
			#for password
		if len(password)<1:
			response['errors'].append('Password is required')
		elif len(password)<8:
			response['errors'].append(' Password must be greater than 8 characters or more')

			#for conf password
		if len(conf_password)<1:
			response['errors'].append('Please confirm the password')
		if conf_password != password:
			response['errors'].append('Confirm password must match password')


		#for dob

		if len(dob)<1:
			response['errors'].append('Date of Birth is required')

		else:
			date=datetime.strptime(dob,'%Y-%m-%d')
			today=datetime.now()
			if date>today:
				response['errors'].append('Date of Birth must be in past ')
		

		if len(response['errors'])>0:
			response['valid']=False

		else:
			user=User.objects.create(
				name=name,
				alias=alias,
				email=email.lower(),
				password=bcrypt.hashpw(password.encode(),bcrypt.gensalt()),
				dob=date,

			)
			response['user']=user

		return response


	def login(self,email,password):

		response={
			'valid':True,
			'errors':[],
			'user':None
		}
		#for email
		if len(email)<1:
			response['errors'].append('Email is required')
		elif not EMAIL_REGEX.match(email):
			response['errors'].append('Email is required')
		else:
			email_list=User.objects.filter(email=email.lower())
			if len (email_list)==0:
				response['errors'].append('Email doesnot exist')
		#for password
		if len(password)<1:
			response['errors'].append('Password is required')
		elif len(password)<8:
			response['errors'].append(' Password must be greater than 8 characters or more')

		if len(response['errors'])==0:
			hashed_pw = email_list[0].password
			if bcrypt.checkpw(password.encode(),hashed_pw.encode()):
				response['user']=email_list[0]
			else:
				response['errors'].append('Incorrect Password')

		if len(response['errors'])>0:
			response['valid']=False

		return response

class QuoteManager(models.Manager):

	def quotesCheck(self,name,content,created_by):

		errors=[]

		if len(name)<1:
			errors.append('Name is required')
		elif len(name)<3:
			errors.append('Name must be greater than 3 characters or more')

		if len(content)<1:
			errors.append('Message is required')
		elif len(content)<10:
			errors.append('Message must br greater than 10 characters or more')

		if len(errors)>0:
			return errors

		else:
			return Quote.objects.create(name=name,content=content,created_by_id=created_by)
		

class User(models.Model):
	name= models.CharField(max_length=255)
	alias=models.CharField(max_length=255)
	email=models.CharField(max_length=255)
	password=models.CharField(max_length=255)
	dob=models.DateField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects=UserManager()

	def __repr__(self):
		return "<User object: {} {} {} {} {}>".format(self.name, self.alias, self.email,self.password,self.dob)


class Quote(models.Model):
	content=models.TextField(max_length=1000)
	name=models.CharField(max_length=255)
	created_by=models.ForeignKey(User,related_name="created_quote")
	created_at=models.DateTimeField(auto_now_add=True)
	objects=QuoteManager()


	def __repr__(self):
		return "<Quote object: {} {} {} {}>".format(self.contant, self.name, self.created_by, self.created_at)


class Favorite(models.Model):
    user = models.ForeignKey(User,related_name='favorited_by')
    quote = models.ForeignKey(Quote, related_name='favorite_quote')

    def __repr__(self):
		return "<Favorite object: {} {}>".format(self.user, self.quote)