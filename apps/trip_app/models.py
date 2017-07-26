# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.db import models
from ..login_app.models import Users
from datetime import datetime
import time
 
class TripManager(models.Manager):
    def add(self, postData, request):
        current = time.strptime(str(datetime.now().date()), "%Y-%m-%d")
        passFlag = True
        if len(postData["destination"]) < 1 or not postData["destination"]:
            messages.error(request, "Destination not valid.")
            passFlag = False
        if len(postData["description"]) < 1 or not postData["description"]:
            messages.error(request, "Description not valid.")
            passFlag = False
        if len(postData["date_from"]) < 1 or not postData["date_from"]:
            messages.error(request, "Travel Date From not valid.")
            passFlag = False
        else:
            date_from = time.strptime(str(postData["date_from"]), "%Y-%m-%d")
            if date_from < current:
                messages.error(request, "Travel From Date has passed already.")
                passFlag = False
        if len(postData["date_to"]) < 1 or not postData["date_to"]:
            messages.error(request, "Travel Date To not valid.")
            passFlag = False
        else:
            date_to = time.strptime(str(postData["date_to"]), "%Y-%m-%d")
            if date_to < date_from or date_to < current:
                messages.error(request, "Can't travel back in time!")
                passFlag = False
        if passFlag:
            trip = Trip.objects.create(user=Users.objects.get(id=request.session["user_id"]), destination=postData["destination"], description=postData["description"], date_from=postData["date_from"], date_to=postData["date_to"])
            return {"trip": trip}
        return {}

class Trip(models.Model):
    user = models.ForeignKey(Users)
    destination = models.CharField(max_length = 100)
    description = models.CharField(max_length = 100)
    date_from = models.DateField()
    date_to = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()

class Joined(models.Model):
    trip = models.ForeignKey(Trip)
    users = models.ManyToManyField(Users, related_name="joined")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)