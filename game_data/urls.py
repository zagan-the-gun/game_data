"""game_data URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from apps.views import index_xxx_game, index_xxx_book, index_thermometer, api, about

urlpatterns = [
    path('', index_xxx_book, name='index_xxx_book'),
    path('xxx_book/', index_xxx_book, name='index_xxx_book'),
    path('xxx_game/', index_xxx_game, name='index_xxx_game'),
    path('thermometer/', index_thermometer, name='index_thermometer'),
#    path('api/', api, name='api'),
    path('about/', about, name='about'),
    path('admin/', admin.site.urls),
]
