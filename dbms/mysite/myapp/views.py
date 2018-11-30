from django.shortcuts import render,redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import (authenticate,get_user_model,logout)
from django.contrib.auth import login as log
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import *
from .forms import *
from.backends import *
# from django.contrib.auth.models import User

User = get_user_model()
# Create your views here.
def index(request):
    return render(request,'myapp/index.html')

def createEvent(request):
    return render(request,'myapp/createEvent.html')
@login_required
def eventScreen(request):
    event = Event.objects.all()
    for e in event:
        print(e.event_name)
    count=1
    return render(request,'myapp/eventScreen.html',{'event':event},{'count':count})

def adminLogin(request):
    return render(request,'myapp/adminLogin.html')

def adminLobby(request):
    return render(request,'myapp/adminLobby.html')

def createAccount(request):
    return render(request,'myapp/createAccount.html')


def login(request):
    return render(request,'myapp/login.html')

def managerLogin(request):
    return render(request,'myapp/managerLogin.html')
@login_required
def paymentLobby(request):
    return render(request,'myapp/paymentLobby.html')

# def signup(request):
#     print("Form is submitted")
#     #cus_id = request.POST["username"]
#     cus_contact = request.POST["cus_contact"]
#     cus_name =request.POST["cus_name"]
#     username =request.POST["username"]
#     password =request.POST["password"]
#     customer= Customer(cus_name=cus_name,cus_contact=cus_contact,username=username,password=password)
#     customer.save()
#     print("Helllloooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
#     return render(request,'myapp/createAccount.html')
#
# def signup_view(request):
#     # form is working but errors are not seen.
#     if request.method =='POST':
#         form = signupform(request.POST)
#         if form.is_valid():
#             form.save()
#             # login(request,username)
#         form = signupform()
#         context = {
#             'form':form
#         }
#
#         return render (request,"myapp/createAccount.html",context)
#
#     else:
#         form = signupform()
#         context = {
#                 'form':form
#             }
#         return render (request,"myapp/createAccount.html",context)
def signup_view(request):
    if request.method =='POST':
        form = signupform(request.POST)
        if form.is_valid():
            form.save()
            # login(request,username)
        form = signupform()
        context = {
            'form':form
        }

        return render (request,"myapp/createAccount.html",context)

    else:
        form = signupform()
        context = {
                'form':form
            }
    return render (request,"myapp/createAccount.html",context)
def login_view(request):
        next = request.GET.get('next')
        if request.method =='POST':
            print('view 1')
            form = loginform(request.POST or None)
            if form.is_valid():
                print('view 2')
                username= form.cleaned_data.get('username')
                password= form.cleaned_data.get('password')
                # user= authenticate(username=username,password=password)
                user = Customer.objects.get(username=username,password=password)
                print(user)
                if user:
                    print(user)
                    log(request,user,backend="myapp.backends.CustomerBackend")
                if next:
                    return redirect(next)
                return redirect('myapp/eventScreen')

            context = {
                    'form':form
                }
            return render (request,"myapp/login.html",context)
        else:
            form = loginform()
            context = {
                    'form':form
                }
            return render (request,"myapp/login.html",context)
def managerLogin_view(request):
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username=form.cleaned_data.get('username')
        password=form.cleaned_data.get('password')
        user=authenticate(username=username,password=password)
        log(request,user)
        if next:
            return redirect(next)
        return redirect('myapp/createEvent')
    context = {
        'form':form
    }
    return render (request,"myapp/managerLogin.html",context)

def managerRegister_view(request):
    next = request.GET.get('next')
    form = ManagerRegistrationForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        log(request,new_user)
        if next:
            return redirect(next)
        return redirect('/')
    context = {
        'form':form
    }
    return render (request,"myapp/managerRegister.html",context)

def logout_view(request):
    logout(request)
    return redirect ('/')

@login_required
def create_event_view(request):
    if request.method =='POST':
        form = eventform(request.POST)
        if form.is_valid():
            form.save()

        context = {
            'form':form
        }
        print ("Event form execution done")
        return render (request,"myapp/createEvent.html",context)

    else:
        form = eventform()
        context = {
                'form':form
            }
        return render (request,"myapp/createEvent.html",context)

# def event_view(request):
#     if request.method =='POST':
#         form = eventform(request.POST)
#         if form.is_valid():
#             form.save()
#
#         context = {
#             'form':form
#         }
#         print ("Hello")
#         return render (request,"myapp/createEvent.html",context)
#
#     else:
#         form = eventform(request.POST)
#         context = {
#                 'form':form
#             }
#         return render (request,"myapp/createEvent.html",context)
