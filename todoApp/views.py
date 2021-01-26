from django.http import response
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.status import *

import json
import datetime
# Create your views here.

def task_list(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/accounts/login')
    
    tasks = Task.objects.filter(author=request.user).order_by('task_created_date')
    return render(request, "todoApp/base.html", {'tasks': tasks})

class NewTaskAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        resp = {}
        try:
            user = request.user
            data = request.data

            data = json.loads(data)

            task_name = data["task_name"]
            task_description = data["task_description"]
            task_category = data["task_category"]
            task_alert_time = data["task_alert_time"]

            task_alert_time = datetime.datetime.strptime(task_alert_time, "%m/%d/%y %H:%M")

            task = Task.objects.create(author=user, task_name=task_name, task_description=task_description, task_category=task_category, task_alert_time=task_alert_time)
            task.add_task()

            return Response(resp, status=HTTP_201_CREATED)
        except Exception as e:
            return Response(resp, status=HTTP_400_BAD_REQUEST)

new_task = NewTaskAPI.as_view()
        