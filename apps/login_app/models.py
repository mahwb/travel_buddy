# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.db import models
import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PW_REGEX = re.compile(r'^([a-zA-Z0-9]{8,15})$')
NAME_REGEX = re.compile(r'^([a-zA-Z]{2,})$')

class UserManager(models.Manager):
    def login(self, postData, request):
        email = postData["email"]
        password = postData["password"]
        user = Users.objects.filter(email=email)
        if not re.match(EMAIL_REGEX, email) or not email:
            messages.error(request, "Enter valid email.")
        else:
            if len(user) == 0:
                messages.error(request, "Email not in database.")
            else: 
                hashed = bcrypt.hashpw(password.encode(), user[0].password.encode())
                if hashed == user[0].password:
                    return {"user": user}
                else:
                    messages.error(request, "Email/Password not valid.")
        return {}

    def register(self, postData, request):
        first_name = postData["first_name"]
        last_name = postData["last_name"]
        email = postData["email"]
        password = postData["password"]
        confirm = postData["confirm"]
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())  
        passFlag = True
        user = Users.objects.filter(email=email)
        if not re.match(NAME_REGEX, first_name) or not first_name:
            passFlag = False
            messages.error(request, "Enter valid first name.")
        if not re.match(NAME_REGEX, last_name) or not last_name:
            passFlag = False
            messages.error(request, "Enter valid last name.")
        if not re.match(EMAIL_REGEX, email) or not email:
            passFlag = False
            messages.error(request, "Enter valid email.")
        if not re.match(PW_REGEX, password) or not password or not confirm:
            passFlag = False
            messages.error(request, "Enter valid password.")
        if password != confirm:
            passFlag = False
            messages.error(request, "Passwords don't match.")     
        if passFlag:
            if len(user) > 0:
                messages.error(request, "User exists.")
            else:
                user = Users.objects.create(first_name=first_name, last_name=last_name, email=email, password=hashed)
                messages.success(request, "Thanks for registering.")

class Users(models.Model):
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    email = models.CharField(max_length = 100)
    password = models.CharField(max_length = 100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()