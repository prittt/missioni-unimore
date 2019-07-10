"""Rimborsi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from RimborsiApp import views, compila_pdf
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.conf.urls import include

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('admin/', admin.site.urls),
    path('profile/', views.profile, name='profile'),
    path('automobili/', views.automobili, name='automobili'),
    path('regolamento/', views.regolamento, name='regolamento'),
    path('crea_missione/', views.crea_missione, name='crea_missione'),
    path('missione/<int:id>', views.missione, name='missione'),
    path('cancella_missione/<int:id>', views.cancella_missione, name='cancella_missione'),
    path('salva_pasti/<int:id>', views.salva_pasti, name='salva_pasti'),
    path('salva_pernottamenti/<int:id>', views.salva_pernottamenti, name='salva_pernottamenti'),
    path('salva_trasporti/<int:id>', views.salva_trasporti, name='salva_trasporti'),
    path('salva_convegni/<int:id>', views.salva_convegni, name='salva_convegni'),
    path('salva_altrespese/<int:id>', views.salva_altrespese, name='salva_altrespese'),

    path('resoconto/<int:id>', views.resoconto, name='resoconto'),
    path('compila_autorizz_dottorandi/<int:id>', compila_pdf.compila_autorizz_dottorandi, name='compila_autorizz_dottorandi'),
    path('genera_pdf/<int:id>', compila_pdf.genera_pdf, name='genera_pdf'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
