from django.contrib import auth
from django.utils.timezone import localdate
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from .models import *
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import authentication
from rest_framework.response import Response
from rest_framework.status import *

import copy
import datetime
import sys


def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('task_list')
        else:
            messages.error(request, "Username and password not correct")
            return redirect('login')
            
    return render(request, "todoApp/login.html")


def signup(request):
    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password == password2:
            try:
                user_exist = User.objects.get(username=username)
            except:
                user_exist = None
            if user_exist:
                messages.error(request, "Username already exists")
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username,
                                     email=email,
                                     password=password)
                user.first_name = firstname
                user.last_name = lastname
                user.save()
            if user:
                user = authenticate(username=username, password=password)
                auth.login(request, user)
                return redirect('task_list')
        else:
            messages.error(request, "Two passwords not matching. Please enter same password in both the fields")
            return redirect('signup')

    return render(request, "todoApp/signup.html")

@login_required
def task_list(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/accounts/login')
    
    tasks = Task.objects.filter(author=request.user).order_by('task_alert_time')
    categories = Category.objects.filter(author=request.user)
    task_count = []
    for category in categories:
        task_count.append(tasks.filter(task_category=category).count())
    categories = zip(categories,task_count)
    temp = copy.deepcopy(categories)
    if len(task_count) > 0:
        temp = list(temp)[0]
        default_cat, default_cat_cnt = temp[0].category_name, temp[1]
    else:
        default_cat, default_cat_cnt = 'Add tasks', 0
    date = localdate()
    for task in tasks:
        due_days = (task.task_alert_time - date).days
        if(due_days < 0):
            setattr(task, "due_days", "0")
        else:
            setattr(task, "due_days", due_days)
    date = date.strftime("%d %B %Y")
    try:
        profile_pic = request.user.profile.photo.url
    except:
        profile_pic = settings.MEDIA_ROOT + '/default_user/default.jpg'
    return render(request, "todoApp/base.html", {'tasks': tasks, 'categories': categories, 'date': date,
                    'default_cat':default_cat ,'default_cat_cnt': default_cat_cnt, 'username': request.user.username, 'profile_pic': profile_pic})


class NewTaskAPI(APIView):
    authentication_classes = [authentication.SessionAuthentication, authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            resp = {}
            user = request.user
            data = request.data
            print(data)

            # data = json.loads(data)

            task_name = data["task_name"]
            task_description = data["task_desc"]
            task_category = data["task_cat"]
            task_alert_time = data["task_alert_time"]

            task_alert_time = datetime.datetime.strptime(task_alert_time, "%Y-%m-%d")

            try:
                category_obj = Category.objects.get(category_name=task_category.lower())
            except Exception as e:
                category_obj = Category.objects.create(author=user,category_name=task_category.lower())
            
            task = Task.objects.create(author=user, task_name=task_name, task_description=task_description, task_category=category_obj, task_alert_time=task_alert_time)
            task.add_task()

            return Response(resp, status=HTTP_201_CREATED)
        except Exception as e:
            print(sys.exc_info())
            return Response(resp, status=HTTP_400_BAD_REQUEST) 

class DeleteTaskAPI(APIView):
    authentication_classes = [authentication.SessionAuthentication, authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]
       
    def post(self, request):
        resp = {}
        try:
            data = request.data
            task_id = data["task_id"]
            try:
                task_obj = Task.objects.get(pk=task_id)
                task_obj.delete()
            except Exception as e:
                return Response(resp, status=HTTP_204_NO_CONTENT)
            return Response(resp, status=HTTP_202_ACCEPTED)
        except Exception as e:
            print(sys.exc_info())
            return Response(resp, status=HTTP_400_BAD_REQUEST) 



class UpdateTaskAPI(APIView):
    authentication_classes = [authentication.SessionAuthentication, authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]
        
    def post(self, request):
        resp = {}
        try:
            data = request.data
            task_id = data["task_id"]
            update_type = data["update_type"]
            try:
                task_obj = Task.objects.get(pk=task_id)
                if update_type == "archieve":
                    task_obj.task_archieved = True
                elif update_type == "done":
                    task_obj.task_done = True
                task_obj.save()
            except Exception as e:
                return Response(resp, status=HTTP_204_NO_CONTENT)
            return Response(resp, status=HTTP_202_ACCEPTED)
        except Exception as e:
            print(sys.exc_info())
            return Response(resp, status=HTTP_400_BAD_REQUEST) 