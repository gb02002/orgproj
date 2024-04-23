"""
URL configuration for orgproj project.

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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from orgproj import settings
from orgs.views import about_view, Map2View


urlpatterns = ([
    path('admin/', admin.site.urls, name='about'),
    path('', Map2View.as_view(), name='map'),
    path('about/', about_view, name='about'),
    path("__debug__/", include("debug_toolbar.urls")),

    path('ur/', include('users.urls')),
    path('lo/', include('orgs.urls')),
               ]
        + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
