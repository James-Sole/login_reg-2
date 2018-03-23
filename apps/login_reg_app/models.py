# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from dateutil.parser import parse as parse_date
from django.db import models
import datetime
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^[a-zA-Z0-9]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z ]+$')

class UserManager(models.Manager):
    def basic_validator(self,postData):
        errors = {}
        if len(postData['name'])<2:
            errors['name']= 'name should be more than 2 characters'
        if not NAME_REGEX.match(postData['name']):
            errors['name_re']= 'name should not contain numbers or simbols'
        if len(postData['username'])<2:
            errors['username']= 'username should be more than 2 characters'
        if not NAME_REGEX.match(postData['username']):
            errors['username_re']= 'username should not contain numbers or simbols'
        if len(postData['password'])<8:
            errors['password']= 'password should be more than 8 characters'
        if not PASSWORD_REGEX.match(postData['password']):
            errors['password_re']= 'password should contain on numbers and characters'
        if postData['password'] != postData['conf_password']:
            errors['conf_password']= 'password should match confirmation password'
        if not EMAIL_REGEX.match(postData['email']):
            errors['email_re']= 'Invalid email'

        return errors
    def login_validator(self,postData):
        errors = {}
        user = User.objects.get(email = postData['username'])
        if postData['username'] == User.username:
            password = user.password
            if not bcrypt.checkpw(postData['password'].encode(), password.encode()):
                error['password'] = 'Incorrect Password'
        else:
            error['username']= 'Incorrect username'
        return errors

class User(models.Model):
    name = models.CharField(max_length = 255)
    username = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    objects = UserManager()

class TripManager(models.Manager):
    def trip_validator(self,postData):
        errors = {}
        dt = parse_date(postData['start'])
        if len(postData['destination'])<2:
            errors['destination']= 'destination should be more than 2 characters'
        if len(postData['description'])<10:
            errors['description']= 'description should be more than 10 characters'
        if dt <= datetime.datetime.now():
            errors['start']= 'the starting date can not be a past date'
        if postData['start']>= postData['end']:
            errors['end']= 'the end date can not be before the end date'
        return errors

class Trip(models.Model):
    destination = models.CharField(max_length = 255)
    description = models.CharField(max_length = 255)
    start_date = models.DateField(null = True)
    end_date = models.DateField(null = True)
    planer = models.ForeignKey(User, related_name="planned_trips")
    users = models.ManyToManyField(User, related_name="trips")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    objects = TripManager()


# Create your models here.
