from django.shortcuts import render, HttpResponse, redirect
from .models import User
from django.contrib import messages


def index(request):
    context = { 'user': User.objects.all() }
    return render(request, 'login_regi/index.html', context)


def regist(request):
    #postData: user's postinfo
    postData = {
        'firstname' : request.POST['firstname'],
        'lastname' : request.POST['lastname'],
        'email' : request.POST['email'],
        'password' : request.POST['password'],
        'password_confirm' : request.POST['password_confirm'],
    }
    #to chekc errors and user info and use sessions 
    errors = User.objects.basic_validator(postData)
    if len(errors) ==0:

        request.session['id'] = User.objects.filter(email=postData['email'])[0].id
        request.session['firstname'] = postData['firstname']
        return redirect('/success')
    else: 
        for errors in errors:
            messages.info(request, errors) 
        return redirect ('/')


def login(request):
    postData = {

    'email' : request.POST['email'],
    'password' : request.POST['password']
    
    }
    #error handler checks user input
    errors = User.objects.login(postData)
    #if theres no errors
    if len(errors) == 0:
        request.session['id'] = User.objects.filter(email=postData['email'])[0].id
        request.session['firstname'] = User.objects.filter(email=postData['email'])[0].firstname
        return redirect('/success')
    for errors in errors:
        messages.info(request, errors)
    return redirect('/')

def success(request):
    context = {
        'users': User.objects.all()
    }
    return render(request, 'login_regi/complete.html', context)


def logout(request):
    #delte id
    del request.session['id']
    del request.session['firstname']

    return redirect('/')