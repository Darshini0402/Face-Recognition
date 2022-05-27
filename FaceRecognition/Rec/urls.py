import imp
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('LoginPage.html',views.login,name='login'),
    path('SignupPage.html',views.signup,name='signup'),
    path('FaceDetect.html',views.facedet,name='facedet'),
    path('DashBoard.html',views.dashboard,name='dashboard'),
]