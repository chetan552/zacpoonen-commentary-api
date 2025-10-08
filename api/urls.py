"""
URL configuration for zac_poonen_commentary_api project.

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
from django.urls import path, include
from api.commentary.views import import_commentaries_view

# Add custom admin URL
original_get_urls = admin.site.get_urls

def new_get_urls():
    urls = original_get_urls()
    my_urls = [
        path('import-commentaries/', admin.site.admin_view(import_commentaries_view), name='import_commentaries'),
    ]
    return my_urls + urls

admin.site.get_urls = new_get_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.commentary.urls')),
]
