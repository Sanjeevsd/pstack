from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("login/", views.loginpage, name="LOGIN"),
    path("logout/", views.logout, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("signup/", views.signup, name="SignUp"),
    path("", views.home, name="HOME"),
    path("home/", views.homepage, name="home"),
    path("home/uploadProject", views.uploadproject),
]
urlpatterns += staticfiles_urlpatterns()

