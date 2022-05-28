from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .FaceLoading import faceload
from .FaceRecognition import facerec
from .AgeDetection import agedet
from django.http.response import HttpResponseRedirect
from django.urls import reverse

# Create your views here.

def home(request):
    return render(request,"HomePage.html")

def login(request):
    global uname
    if request.method == "POST":
        uname=request.POST["username"]
        pswd=request.POST["password"]     
        u = User.objects.get(username__exact = uname)
        if u.check_password(pswd):
            if(facerec.facecomp(uname)):
                return HttpResponseRedirect(reverse("dashboard"))
            else:
                return render(request, "LoginPage.html",{"message":"Unauthorized access"})
        else:
            return render(request, "LoginPage.html",{"message":"Invalid credentials"})

    return render(request,"LoginPage.html")

def signup(request):
    return render(request,"SignupPage.html")

def facedet(request):
    if request.method == "POST":
        uname=request.POST["username"]
        fname=request.POST["fname"]
        lname=request.POST["lname"]
        email=request.POST["email"]
        pswd=request.POST["password"]     

        if User.objects.filter(username=uname).exists():
            return render(request, "SignupPage.html",{"message":"Username already exists"})

        else:
            new_user = User.objects.create_user(uname,email,pswd,first_name=fname,last_name=lname)
            new_user.save()
            new_user.is_active = False  
            faceload.facesave(uname)
            return HttpResponseRedirect(reverse("login"))   

    return render(request,"FaceDetect.html")

def dashboard(request):
    age_val = agedet.predict_age()
    return render(request,"DashBoard.html",{"age":age_val,"name":uname})