from os import name
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("login/", views.loginpage, name="LOGIN"),
    path("logout/", views.logout, name="logout"),
    path("updateProfile/", views.updateProfile, name="profile"),
    path("signup/", views.signup, name="SignUp"),
    path("", views.home, name="HOME"),
    path("viewpdf/",views.viewPDF,name="PDFVIEW"),
    path("home/", views.homepage, name="home"),
    path("uploadProject/", views.uploadproject),
    path("home/contact/", views.contacts, name="Contacts"),
]
urlpatterns += staticfiles_urlpatterns()
