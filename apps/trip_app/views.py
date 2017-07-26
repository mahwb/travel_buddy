# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Users, Trip, Joined
from django.shortcuts import render, redirect
from django.contrib import messages

# shows index page
def index(request):
    if not request.session["logged_in"]:
        messages.error(request, "Please log in.")
        return redirect("login:idx")
    # get joined trip ids
    exclude = []
    joined = Joined.objects.all().filter(users__id=request.session["user_id"])
    for join in joined:
        exclude.append(join.trip.id)
    data = {
        "mytrips": Trip.objects.all().filter(user__id=request.session["user_id"]),
        "joined": joined,
        "unjoined": Trip.objects.all().exclude(id__in=exclude)
    }
    return render(request, "trip_app/index.html", data)

# shows add page
def add(request):
    if not request.session["logged_in"]:
        messages.error(request, "Please log in.")
        return redirect("login:idx")
    return render(request, "trip_app/add.html")

# shows destination page
def dest(request, id):
    if not request.session["logged_in"]:
        messages.error(request, "Please log in.")
        return redirect("login:idx")
    data = {
        "trip": Trip.objects.get(id=id),
        "users": Users.objects.all().filter(joined__trip__id=id)
    }
    return render(request, "trip_app/destination.html", data)

# creates new trip plan
def new(request):
    if not request.session["logged_in"]:
        messages.error(request, "Please log in.")
        return redirect("login:idx")
    trip = Trip.objects.add(request.POST, request)
    if "trip" in trip:
        return redirect("trip:idx")
    else:
        return redirect("trip:add")

# joins trip
def join(request, id):
    if not request.session["logged_in"]:
        messages.error(request, "Please log in.")
        return redirect("login:idx")
    # check if joined already
    if len(Joined.objects.filter(trip__id=id).filter(users__id=request.session["user_id"])) < 1:
        user = Users.objects.get(id=request.session["user_id"])
        trip = Joined.objects.create(trip=Trip.objects.get(id=id))
        trip.users.add(user)
    return redirect("trip:idx")