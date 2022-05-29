from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .FaceLoading import faceload
from .FaceRecognition import facerec
from .AgeDetection import agedet
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from .models import Movie
from django.db.models import Q

# Create your views here.

def home(request):
    return render(request,"HomePage.html")

def login(request):
    global name
    if request.method == "POST":
        uname=request.POST["username"]
        pswd=request.POST["password"]   
        try:  
            u = User.objects.get(username__exact = uname)
            name = u.first_name
            if u.check_password(pswd):
                if(facerec.facecomp(uname)):
                    return HttpResponseRedirect(reverse("dashboard"))
                else:
                    return render(request, "LoginPage.html",{"message":"Unauthorized access"})
            else:
                return render(request, "LoginPage.html",{"message":"Invalid credentials"})
        except:
            return render(request, "LoginPage.html",{"message":"User does not exist"})

    return render(request,"LoginPage.html")

def signup(request):
    return render(request,"SignupPage.html")

def facedet(request):
    global uname
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
            return HttpResponseRedirect(reverse("facedet"))
    else:
        if(faceload.facesave(uname)):
            return HttpResponseRedirect(reverse("login"))
        return render(request,"FaceDetect.html")

def dashboard(request):
    age_val = agedet.predict_age()
   
    l_age = int(age_val[1])*10 + int(age_val[2])
    u_age = int(age_val[5])*10 + int(age_val[6])

    movie_list = Movie.objects.filter(Q(lower_age__lte=l_age) & Q(upper_age__gte=u_age))
    
    return render(request,"DashBoard.html",{"name":name,"movie_custom":movie_list,"movies":Movie.objects.all(),"n":3})