from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.models import auth, User
from django.contrib import messages
from nltk.util import pr
from . import pdftext
from rest_framework import viewsets
from .models import usersprofile
from django.http import JsonResponse
from django.forms.models import model_to_dict
from .models import usersprofile, projects
import json, random
from django.core import serializers
from django.contrib.auth.decorators import login_required


def loginpage(request):
    if request.method == "POST":
        Username = request.POST.get("Username")
        Password = request.POST.get("Password")
        user = auth.authenticate(username=Username, password=Password)
        if user is not None:
            auth.login(request, user)
            greetings = [
                f"Hello @{user.username}, Welcome back",
                f"Hi there @{user.username},Glad you came back",
                f"Hi there @{user.username},It's good to see you again"
            ]
            messages.add_message(request, 159, random.choices(greetings)[0])
            return HttpResponseRedirect("/")
        else:
            message = "Invalid Email or Password"
            messages.add_message(
                request, 951, "Couldn't Login, Invalid Username or Password")
            return render(request, "login.html")
    else:
        return render(request, "login.html")


def signup(request):
    if request.method == "POST":
        try:
            user = User.objects.get(username=request.POST["Username"])
            if user is not None:
                E_message = f"Invalid username: {user} already taken"
                messages.add_message(request, 951, E_message)
                return render(request, "reg.html")

        except User.DoesNotExist:
            Username = request.POST["Username"]
            Password = request.POST["Password"]
            email = request.POST["email"]
            ConfirmPassword = request.POST["ConfirmPassword"]
            if Password == ConfirmPassword:
                user = User.objects.create_user(
                    email=email,
                    username=Username,
                    password=Password,
                    first_name=Username,
                )
                user.save()
                messg = f"User {user} registered successfully"
                messages.add_message(request, 159, messg)
                user = auth.authenticate(username=Username, password=Password)
                return redirect("/")
            else:
                message = "Password are not same"
                messages.add_message(request, 951, message)
                return render(request, "reg.html")
    else:
        return render(request, "reg.html")


@login_required(login_url='/login')
def homepage(request):
    if request.user.is_authenticated:
        all_projects = {}
        recommended_projects = {}
        popular_projects = {}
        my_projects = {"a": projects.objects.filter(user=request.user)}

        return render(request, "homem.html", my_projects)
    else:
        return HttpResponseRedirect("/login")


@login_required(login_url='/login')
def home(request):
    return HttpResponseRedirect("/home")


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/login")


@login_required
def uploadproject(request):
    if request.method == "POST":
        file = request.FILES["projectfile"]
        title, body = pdftext.pdf_to_txt(file)
        if title == "error":
            messages.error(request, f"Invalid Project File {file}")
            return HttpResponseRedirect("/")

        project_update = projects(user=request.user,
                                  projectname=title,
                                  contents=body)
        project_update.save()
        project = projects.objects.filter(user=request.user)
        # questions_by_category = [question.__dict__ for question in questions_by_category]
        serialized_data = {}
        for p in project:
            serialized_data[p.projectname] = serializers.serialize('json', [p])

        return JsonResponse({"Projects": serialized_data})
    elif request.method == "GET":
        return HttpResponseRedirect('/')


@login_required
def updateProfile(request):
    if request.method == 'POST':
        formData = json.loads(request.POST.get('serialData'))
        form_data_dict = {}
        for field in formData:
            form_data_dict[field["name"]] = field["value"]
        skills = form_data_dict['skills']
        interests = form_data_dict['interests']
        aboutme = form_data_dict['aboutme']
        fblink = form_data_dict['fblink']
        gitlink = form_data_dict['gitlink']
        usermodel = usersprofile.objects.get(user=request.user)
        if request.POST.get("ifimage") != "none":
            usermodel.avatar = request.FILES['image_form']

        usermodel.skills = skills
        usermodel.skillsinterests = interests
        usermodel.skillsaboutme = aboutme
        usermodel.skillsfblink = fblink
        usermodel.skillsgitlink = gitlink
        try:
            usermodel.save()
        except:
            response = JsonResponse({"errors": "Invalid Image File"})
            response.status_code = 400
            return response

        returnData = {
            "skills": skills,
            "interests": interests,
            "aboutme": aboutme,
            "fblink": fblink,
            "gitlink": gitlink
        }
        return JsonResponse({"userprofile": returnData})


# success=159, error=951, warn=357, info=753