from django.urls import path
from RimborsiApp import views, compila_pdf, utils
from django.conf.urls import include

app_name = 'RimborsiApp'
urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('foreign_profile/', views.foreign_profile, name='foreign_profile'),
    path('automobili/', views.automobili, name='automobili'),
    path('regolamento/', views.regolamento, name='regolamento'),
    path('crea_missione/', views.crea_missione, name='crea_missione'),
    path('lista_missioni/', views.lista_missioni, name='lista_missioni'),
    path('missione/<int:id>', views.missione, name='missione'),
    path('clona_missione/<int:id>', views.clona_missione, name='clona_missione'),
    path('concludi_missione/<int:id>', views.concludi_missione, name='concludi_missione'),
    path('cancella_missione/<int:id>', views.cancella_missione, name='cancella_missione'),
    path('salva_pasti/<int:id>', views.salva_pasti, name='salva_pasti'),
    path('salva_pernottamenti/<int:id>', views.salva_pernottamenti, name='salva_pernottamenti'),
    path('salva_trasporti/<int:id>', views.salva_trasporti, name='salva_trasporti'),
    path('salva_convegni/<int:id>', views.salva_convegni, name='salva_convegni'),
    path('salva_altrespese/<int:id>', views.salva_altrespese, name='salva_altrespese'),

    path('resoconto/<int:id>', views.resoconto, name='resoconto'),
    path('compila_autorizz_dottorandi/<int:id>', compila_pdf.compila_autorizz_dottorandi,
         name='compila_autorizz_dottorandi'),
    path('genera_pdf/<int:id>', compila_pdf.genera_pdf, name='genera_pdf'),

    path('invia_email_autorizzazione/<int:id>', views.invia_email_autorizzazione, name='invia_email_autorizzazione'),

    path('download/<int:id>/<str:field>', utils.download, name='download'),

    path('statistiche', views.statistiche, name='statistiche'),
]
