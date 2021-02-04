from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/logout/', views.LogoutView.as_view(next_page='/todo/accounts/login'), name='logout'),
    path('', include('todoApp.urls')),
    path('todo/', include('todoApp.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
