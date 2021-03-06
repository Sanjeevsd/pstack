from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.models import auth, User
from django.contrib import messages
from pandas.core.base import DataError
from . import pdftext
from django.core.files.storage import FileSystemStorage
import pandas as pd
from django.http import FileResponse, Http404
import joblib
from django.http import JsonResponse
from django.forms.models import model_to_dict
from .models import usersprofile, projects, ContactForm
import json, random
from django.core import serializers
from django.contrib.auth.decorators import login_required
from csv import writer

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
        tags=joblib.load('clusters.pkl')
        user_cluster=tags[request.user.usersprofile.cluster]
        df=pd.read_csv('indexedReport.csv')
        recommended_projects = {}
        popular_projects = {}
                
        clusters=joblib.load('clusters.pkl')
        data1=clusters[0]
        for a,d2 in clusters.items():
                l1=[]
                l2=[]
                unions=data1+d2
                for w in unions: 
                        if w in data1: l1.append(1)
                        else: l1.append(0) 
                        if w in d2: l2.append(1) 
                        else: l2.append(0) 
                c = 0
                for i in range(len(unions)): 
                        c+= l1[i]*l2[i] 
                cosine = c / float((sum(l1)*sum(l2))**0.5) 
                if(cosine>0.4):
                        data1=list(set(data1)|set(d2))
        ptag=data1
        kmeans=joblib.load('Kmodel.pkl')
        tfidf=joblib.load('TFIDF.pkl')
        pop_pred_vec=tfidf.transform(["".join(data1)])
        pop_pred=kmeans.predict(pop_pred_vec)
        print(pop_pred[0])
        for index, row in df.iterrows():
            d=row.to_dict()
            ap={}
            ap['title']=d['title']
            ap['fname']=d['fname']
            ap['features']=tags[d['label']]
            all_projects[index]=ap
            proj={}
            pop_proj={}
            if d['label']==request.user.usersprofile.cluster:
                proj['title']=d['title']
                proj['fname']=d['fname']
                proj['features']=user_cluster        
                recommended_projects[index]=proj
            if d['label']==pop_pred[0]:
                pop_proj['title']=d['title']
                pop_proj['fname']=d['fname']
                pop_proj['features']="TAGS"        
                popular_projects[index]=pop_proj
                

        my_projects = {"a": projects.objects.filter(user=request.user)}

        return render(request, "homem.html", {'ptag':ptag,'pop_project':popular_projects,'allproj':all_projects,'my_projects':my_projects,'features':user_cluster,'recommend':recommended_projects})
    else:
        return HttpResponseRedirect("/login")


@login_required(login_url='/login')
def home(request):
    return HttpResponseRedirect("/home")


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/login")

@login_required
def contacts(request):
    if request.method == 'POST':
        FirstName = request.POST["FirstName"]
        LastName = request.POST["LastName"]
        Email = request.POST["Email"]
        Message = request.POST["Message"]
        print(FirstName)
        contact_obj = ContactForm(FirstName=FirstName, LastName=LastName, Email=Email, Message=Message)
        contact_obj.save()
        return HttpResponseRedirect("/")

@login_required
def uploadproject(request):
    if request.method == "POST":
        kmeans=joblib.load('Kmodel.pkl')
        tfidf=joblib.load('TFIDF.pkl')
        file = request.FILES["projectfile"]
        title, body = pdftext.pdf_to_txt(file)
        if title == "error":
            messages.error(request, f"Invalid Project File {file}")
            return HttpResponseRedirect("/")
        fs=FileSystemStorage()
        fs.save(file.name,file)
        tfidfvector=tfidf.transform([body])
        predct_kmean=kmeans.predict(tfidfvector)
        data = pd.read_csv('indexedReport.csv') 
        totalInstances=len(data)+1
        ls=[totalInstances, file.name,title,body,predct_kmean[0]]
        with open('indexedReport.csv','a',newline='') as reports:
            writer_obj=writer(reports)
            writer_obj.writerow(ls)
        project_update = projects(user=request.user,
                                  projectname=title,
                                  contents=body)
        project_update.save()
        project = projects.objects.filter(user=request.user)
        serialized_data = {}
        for p in project:
            serialized_data[p.projectname] = serializers.serialize('json', [p])

        return JsonResponse({"Projects": serialized_data})
    elif request.method == "GET":
        return HttpResponseRedirect('/')

@login_required
def viewPDF(request):
    if request.method=='POST':
        dirt=request.POST.get('fname')
        print(dirt)
        try:
            return FileResponse(open('{}'.format(dirt), 'rb'), content_type='application/pdf')
        except FileNotFoundError:
            raise Http404()
    else:
        raise Http404()

@login_required
def updateProfile(request):
    if request.method == 'POST':
        formData = json.loads(request.POST.get('serialData'))
        form_data_dict = {}
        for field in formData:
            form_data_dict[field["name"]] = field["value"]
        skills = form_data_dict['skills']
        interests = form_data_dict['interests']
        kmeans=joblib.load('Kmodel.pkl')
        tfidf=joblib.load('TFIDF.pkl')
        vectorize=tfidf.transform([interests])
        prediction_cluster=kmeans.predict(vectorize)
        recomm_cluster=prediction_cluster[0]
        aboutme = form_data_dict['aboutme']
        fblink = form_data_dict['fblink']
        gitlink = form_data_dict['gitlink']
        usermodel = usersprofile.objects.get(user=request.user)
        if request.POST.get("ifimage") != "none":
            usermodel.avatar = request.FILES['image_form']
        usermodel.cluster=recomm_cluster
        usermodel.skills = skills
        usermodel.interests = interests
        usermodel.aboutme = aboutme
        usermodel.fblink = fblink
        usermodel.gitlink = gitlink
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