from django.urls import path
from . import views


urlpatterns = [
    path('accounts/login/', views.login, name='login'),
    path('accounts/signup/', views.signup, name='signup'),
    path('', views.task_list, name='task_list'),
    path('add_task/', views.NewTaskAPI.as_view(), name='new_task'),
    path('delete_task/', views.DeleteTaskAPI.as_view(), name='delete_task'),
    path('update_task/', views.UpdateTaskAPI.as_view(), name='update_task'),
]