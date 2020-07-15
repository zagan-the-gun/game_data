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
from apps.views import about, index, index_default, index_large_default, item_redirect
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import url
from django.views.generic.base import RedirectView


urlpatterns = [
    path('', index, name='index'),
    path('default_about/', about, name='about'),
    path('admin/', admin.site.urls),
    path('stock-news/', index_large_default, name='index_large_default'),
    path('stock-news/<str:l_category>/', index_default, name='index_default'),
    path('stock-news/<str:l_category>/<str:m_category>/', index_default, name='index_default'),
    path('stock-news/<str:l_category>/<str:m_category>/<str:s_category>/', index_default, name='index_default'),
    path('product/<int:item_id>', item_redirect, name='item_redirect'),
    #いずれ消す
    path('alcohol_spray/', index, name='index'),
    path('alcohol_gel/', index, name='index'),
    path('thermometer/', index, name='index'),
    path('about/', index, name='index'),
#    url(r'^.*$', RedirectView.as_view(url='/', permanent=True)),
]

#urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#urlpatterns += url(r'^.*$', RedirectView.as_view(url='/', permanent=True))

