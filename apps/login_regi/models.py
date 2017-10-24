from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
import re
import md5
import os, binascii
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX =re.compile('^[A-z]+$')

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = []

        if len(postData['firstname']) < 2:
            errors.append("First Name should be more than 2 characters")
        elif not NAME_REGEX.match(postData['firstname']):
            errors.append("Invalid letter")
        if len(postData['lastname']) < 2:
            errors.append("Last Name should be more than 2 characters")
        elif not NAME_REGEX.match(postData['lastname']):
            errors.append("Invalid letter")
        if len(postData['email']) < 2:
            errors.append("Email should be more than 2 characters")
        elif not EMAIL_REGEX.match(postData['email']):
            errors.append("Email invalid")
        if len(postData['password']) < 8:
            errors.append("Password should be more than 10 characters")
        elif postData['password'] != postData['password_confirm']:
            errors.append("Password is not matched")
            
#if there's no error then password 
        if len(errors) == 0 :
             # if email is found in db
            salt = binascii.b2a_hex(os.urandom(15)) 
            hashed_pw = md5.new(salt + postData['password']).hexdigest()
             # add to database
            User.objects.create(firstname=postData['firstname'], lastname=postData['lastname'], email=postData['email'], salt=salt, password=hashed_pw)

        return errors

    def login(self, postData):
        errors = []
        # if email is found in db
        if User.objects.filter(email=postData['email']):
            salt = User.objects.get(email=postData['email']).salt
            hashed_pw = md5.new(salt + postData['password']).hexdigest()
            # compare hashed passwords
            if User.objects.get(email=postData['email']).password != hashed_pw:
                errors.append('Incorrect password')
        # else if email is not found in db
        else:
            errors.append('Email has not been registered')
        return errors



class User(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    salt = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    def __repr__(self):
        return "user object: ---,{} ----{}, ----{}".format(self.firstname, self.lastname, self.email)