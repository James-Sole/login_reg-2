# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect, reverse
from django.contrib import messages
from models import *
import bcrypt
def index(request):
	return render(request, "login_reg_app/index.html")
def login(request, methods = ['POST']):
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request,error)
        return redirect('/')
    request.session['id']= User.objects.get(email = request.POST['email']).id
    request.session['status']= 'logged in'
    return redirect('/trips')

def register(request, methods = ['POST']):
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request,error)
        return redirect('/')
    password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    User.objects.create(name = request.POST['name'], username = request.POST['username'], email = request.POST['email'], password = password)
    request.session['id']= User.objects.last().id
    request.session['status']= 'registered'
    return redirect('/trips')

def trips(request):
    if 'id' in request.session:
        context = {
            'username' : User.objects.get(id =request.session['id']).username,
            'my_trips' : Trip.objects.filter(users = request.session['id']),
			'other_trips' : Trip.objects.exclude(users = request.session['id']) ,
        }
        return render(request, "login_reg_app/success.html", context)
    return redirect('/')

def tripsId(request, id):
    if 'id' in request.session:
        context = {
            'trip' : Trip.objects.get(id = id),
			'others' : Trip.objects.get(id = id).users ,
        }
        return render(request, 'login_reg_app/trips.html', context)
    return redirect('/')

def tripsAdd(request):
    if 'id' in request.session:
        return render(request, 'login_reg_app/add.html')
    return redirect('/')

def add(request, methods = ['POST']):
    errors = Trip.objects.trip_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request,error)
        return redirect('/trips/add')
	user = User.objects.get(id =request.session['id'])
	#create_trip
	Trip.objects.create(destination = request.POST['destination'], description= request.POST['description'], start_date=request.POST['start'], end_date=request.POST['end'] , planer= user)
	#add user to trip
	request.session['trip'] = Trip.objects.last().id
	trip = Trip.objects.get(id = request.session['trip'])
	trip.User.add(user)
    return redirect('/trips')

def join(request, id):
	#add user to trip
	user = User.objects.get(id =request.session['id'])
	trip = Trip.objects.get(id = id)
	trip.User.add(user)
	return redirect('/trips')

def logout(request):
    request.session.clear()
    return redirect('/')


# Create your views here.
