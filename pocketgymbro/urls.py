"""
URL configuration for pocketgymbro project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from gymapp import views as gymappViews
from gymapp import views
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import views as auth_views


from django.conf.urls.static import static
from django.conf import settings

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', gymappViews.home, name='Home'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='index.html'), name='login'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
