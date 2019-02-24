# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


from django.shortcuts import render_to_response
from django.http import HttpResponseBadRequest, HttpResponse
from django import forms
from django.template import RequestContext
from models import *
import xlrd
import datetime
from datetime import timedelta
import pdb
from networkingapp import settings
import stripe
from django.contrib import messages
from forms import SignUpForm

stripe.api_key = settings.STRIPE_SECRET_KEY
# Create your views here.

def home(request):
    return render(request, 'networking/homess.html')

def pricing(request):
    context = { "stripe_key": settings.STRIPE_PUBLIC_KEY }
    if request.method == "POST":
        print "Post"
        for key, values in request.POST.lists():
            print(key, values)
        print request.POST.get('emailname')
        email = request.POST.get('emailname')
        a = emailcapture(email = email)
        a.save()
        messages.success(request, "You're all signed up! We'll let you know when we are taking more people.")
    return render(request, 'networking/pricing.html', context)

def pricingwcheckout(request):
    context = { "stripe_key": settings.STRIPE_PUBLIC_KEY }
    if request.method == "POST":
        print "Post"
        for key, values in request.POST.lists():
            print(key, values)
        print request.POST.get('emailname')
        email = request.POST.get('emailname')
        a = emailcapture(email = email)
        a.save()
        messages.success(request, "You're all signed up! We'll let you know when we are taking more people.")
    return render(request, 'networking/pricingwcheckout.html', context)

def howitworks(request):
    return render(request, 'networking/howitworks.html')

def checkout(request):
    if request.method == "POST":
        token    = request.POST.get("stripeToken")
        print (token)
    try:
        charge  = stripe.Charge.create(
            amount      = 1000,
            currency    = "usd",
            source      = token,
            description = "Inital product "
        )

#        new_car.charge_id   = charge.id

    except stripe.error.CardError as ce:
        return False, ce

    else:
#        new_car.save()
        return redirect("/getstarted/")
        # The payment was successfully processed, the user's card was charged.
        # You can now redirect the user to another page or whatever you want

def getstarted(request):
    if request.method == 'POST':
        if 'signup' in request.POST:
            for key, values in request.POST.lists():
                print(key, values)
            form = SignUpForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('email')
                raw_password = form.cleaned_data.get('password1')
                user = User.objects.create_user(username, username, raw_password)
                user.first_name = form.cleaned_data.get('first_name')
                user.last_name = form.cleaned_data.get('last_name')
                user.save()
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect('/getstarted/')
        elif 'login' in request.POST:
                email = request.POST['email']
                password = request.POST['password']
                user = authenticate(username=email, password=password)
                if user is not None:
                    login(request, user)
                return redirect('/getstarted/')
        elif 'upload' in request.POST:
            form = UploadFileForm(request.POST,request.FILES)
            if form.is_valid():
                filehandle = request.FILES['file']
                sheet1 = filehandle.get_sheet()
#                del sheet1.column[6]
#                del sheet1.column[5]
#                sheet1.column += ['User']
                sheet1.save_as('newdoc.xls')
                workbook = xlrd.open_workbook('newdoc.xls')
                worksheet = workbook.sheet_by_index(0)
                rownum = worksheet.nrows
                print rownum
                i = 1
                while i < rownum:
                    owner = request.user
                    first_name = worksheet.cell(i,0).value
                    last_name = worksheet.cell(i,1).value
                    email = worksheet.cell(i,2).value
                    company = worksheet.cell(i,3).value
                    position = worksheet.cell(i,4).value
                    connection_level = 3
                    dated_connected = worksheet.cell(i,5).value
                    con = Connection(first_name = first_name, last_name = last_name, email = email, company = company, position = position, connection_level = connection_level, owner=owner)
                    con.save()
                    date = datetime.date.today()
                    dateoneweek = date + timedelta(weeks=1)
                    x = Week(owner = owner, number = 1)
                    x.save()
                    w=0
                    while (date < dateoneweek) and (w<1):
                        a = ToContact.objects.filter(date = date)
                        if a:
                            date = date + timedelta(days = 1)
                            print date
                        else:
                            q = ToContact(connection = con, date = date)
                            q.save()
                            x.contacts.add(q)
                            print 'scheduled'
                            w=1
                    i = i+1
#                newsheet = pe.get_sheet(file_name='newdoc.csv', name_columns_by_row=0)
#                newsheet.save_to_django_model(model=Connection, initializer=choice_func, mapdict=['first_name', 'last_name', 'email', 'company', 'position', 'owner'])
                return redirect('/nextsteps/')
            else:
                return HttpResponseBadRequest()
    else:
        form = SignUpForm()
        uploadform = UploadFileForm()
    return render(
        request,
        'networking/getstarted.html',
        {'uploadform': uploadform,
        'form': form}
        )
#def import_sheet(request):
#    return render(request, 'networking/home.html')

#signup form and view from https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html
def signup(request):
    if request.method == 'POST':
        for key, values in request.POST.lists():
            print(key, values)
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = User.objects.create_user(username, username, raw_password)
            user.save()
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def categorize(request):
    people = Connection.objects.filter(owner = request.user)
    if request.method == "POST":
        for key, value in request.POST.items():
            connection = Connection.objects.filter(owner = request.user, email = key)
            if connection:
                connectionlvlold = unicode(connection[0].connection_level)
                if connectionlvlold == value:
                    pass
                else:
                    connection[0].connection_level = value
                    connection[0].save()
    return render(request, 'networking/categorize.html', {'people': people})

class UploadFileForm(forms.Form):
    file = forms.FileField()

def import_sheet(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST,
                              request.FILES)
        if form.is_valid():
            filehandle = request.FILES['file']
            sheet1 = filehandle.get_sheet()
#            del sheet1.column[6]
#            del sheet1.column[5]
#            sheet1.column += ['User']
            sheet1.save_as('newdoc.xls')
            workbook = xlrd.open_workbook('newdoc.xls')
            worksheet = workbook.sheet_by_index(0)
            rownum = worksheet.nrows
            print rownum
            i = 1
            while i < rownum:
                owner = request.user
                first_name = worksheet.cell(i,0).value
                last_name = worksheet.cell(i,1).value
                email = worksheet.cell(i,2).value
                company = worksheet.cell(i,3).value
                position = worksheet.cell(i,4).value
                connection_level = 3
                dated_connected = worksheet.cell(i,5).value
                con = Connection(first_name = first_name, last_name = last_name, email = email, company = company, position = position, connection_level = connection_level, owner=owner)
                con.save()
                date = datetime.date.today()
                dateoneweek = date + timedelta(weeks=1)
                x = Week(owner = owner, number = 1)
                x.save()
                w=0
                while (date < dateoneweek) and (w<1):
                    a = ToContact.objects.filter(date = date)
                    if a:
                        date = date + timedelta(days = 1)
                        print date
                    else:
                        q = ToContact(connection = con, date = date)
                        q.save()
                        x.contacts.add(q)
                        print 'scheduled'
                        w=1
                i = i+1
#            newsheet = pe.get_sheet(file_name='newdoc.csv', name_columns_by_row=0)
#            newsheet.save_to_django_model(model=Connection, initializer=choice_func, mapdict=['first_name', 'last_name', 'email', 'company', 'position', 'owner'])
            return HttpResponse("OK")
        else:
            return HttpResponseBadRequest()
    else:
        uploadform = UploadFileForm()
    return render(
        request,
        'networking/upload_form.html',
        {'uploadform': uploadform})

#rownum = worksheet.nrows
#i = 1
#while i < rownum:
##    user = request.user
#    owner = User.objects.get(username='gene.sussman+1@gmail.com')
#    first_name = worksheet.cell(i,0).value
#    last_name = worksheet.cell(i,1).value
#    email = worksheet.cell(i,2).value
#    company = worksheet.cell(i,3).value
#    position = worksheet.cell(i,4).value
#    connection_level = 3
#    dated_connected = worksheet.cell(i,5).value
#    con = Connection(first_name = first_name, last_name = last_name, email = email, company = company, position = position, connection_level = connection_level, owner=owner)
#    con.save()
#    i = i+1#

def signup_manual(request):
    if request.method == 'POST':
        result = request.POST
        for key, values in request.POST.lists():
            print(key, values)
        username = request.POST['email']
        email = request.POST['email']
        password = request.POST['password']
        firstname = request.POST['first_name']
        lastname = request.POST['last_name']
        user = User.objects.create_user(username = username, email = email, password = password, first_name = firstname, last_name = lastname)
        user.save()
        userlogin = authenticate(username=username, password=password)
        login(request, userlogin)
        return redirect('/update-profile/')
#            user = form.save()
#            user.refresh_from_db()  # load the profile instance created by the signal
#            user.profile.name = form.cleaned_data.get('name')
#            user.profile.description = form.cleaned_data.get('description')
#            user.profile.topic = form.cleaned_data.get('topic')
#            user.profile.twitter_link = form.cleaned_data.get('twitter_link')
#            user.profile.twitter_follower = form.cleaned_data.get('twitter_follower')
#            user.profile.facebook_link = form.cleaned_data.get('twitter_link')
#            user.profile.facebook_follower = form.cleaned_data.get('twitter_follower')
#            user.profile.instagram_link = form.cleaned_data.get('twitter_link')
#            user.profile.instagram_follower = form.cleaned_data.get('twitter_follower')
#            user.profile.youtube_link = form.cleaned_data.get('twitter_link')
#            user.profile.youtube_follower = form.cleaned_data.get('twitter_follower')
#            user.profile.image = form.cleaned_data.get('image')
#            user.save()
#            raw_password = form.cleaned_data.get('password1')
#            user = authenticate(username=user.username, password=raw_password)
#            login(request, user)
    else:
        return render(request, 'registration/signup.html', {'form': form})
        
def nextsteps(request):
    connections = Connection.objects.filter(owner=request.user)
    return render(request, 'networking/nextsteps.html', {'connections':connections})