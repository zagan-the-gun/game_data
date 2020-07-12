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
from apps.views import index_xxx_game, index_xxx_book, api, about, index, index_kaisen, index_default, index_large_default
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import url
from django.views.generic.base import RedirectView


urlpatterns = [
    path('', index, name='index'),
    path('xxx_book/', index_xxx_book, name='index_xxx_book'),
    path('xxx_game/', index_xxx_game, name='index_xxx_game'),
    path('kaisen_kani/', index_kaisen, name='index_kaisen'),
    path('kaisen_ebi/', index_kaisen, name='index_kaisen'),
    path('kaisen_kaki/', index_kaisen, name='index_kaisen'),
    #path('api/', api, name='api'),
    path('about/', about, name='about'),
    path('kaisen_about/', about, name='about'),
    path('default_about/', about, name='about'),
    path('admin/', admin.site.urls),
    path('stock-news/', index_large_default, name='index_large_default'),
    path('stock-news/<str:l_category>/', index_default, name='index_default'),
    path('stock-news/<str:l_category>/<str:m_category>/', index_default, name='index_default'),
    path('stock-news/<str:l_category>/<str:m_category>/<str:s_category>/', index_default, name='index_default'),
#    path(r'^.*$', index_large_default, name='index_large_default'),
    url(r'^.*$', RedirectView.as_view(url='stock-news/', permanent=True)),
#    url(r'^.*$', index_large_default, name='index_large_default'),
]

#urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

