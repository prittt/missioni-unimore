from django.urls import path
from RimborsiApp import views, compila_pdf, utils
from django.conf.urls import include

from django.conf.urls.static import static
from django.conf import settings

app_name = 'RimborsiApp'
urlpatterns = [
    path('serve_signature/<int:id>', utils.serve_signature, name='serve_signature'),
    path('firma_received_visualization/', views.firma_received_visualization, name='firma_received_visualization'),
    path('firma_shared/', views.firma_shared, name='firma_shared'),
    path('firma/', views.firma, name='firma'),
    path('profile/', views.profile, name='profile'),
    path('foreign_profile/', views.foreign_profile, name='foreign_profile'),
    path('italian_profile/', views.italian_profile, name='italian_profile'),
    path('automobili/', views.automobili, name='automobili'),
    path('regolamento/', views.regolamento, name='regolamento'),
    path('crea_missione/', views.crea_missione, name='crea_missione'),
    path('lista_missioni/', views.lista_missioni, name='lista_missioni'),
    path('collaboratori/', views.collaboratori, name='collaboratori'),
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

    path('maintenance/', views.maintenance, name='maintenance'),

    path('media/users/<int:id1>/<int:id2>/<str:field1>/<str:field2>', utils.secure_media),
    path('spese_image_preview/<int:id>', utils.spesa_image_preview, name='spese_image_preview'),

    path('trasporti_image_preview/<int:id>', utils.trasporto_image_preview, name='trasporti_image_preview'),
    path('pasto_image_preview/<int:id>/<str:img_field_name>/', utils.pasto_image_preview, name='pasto_image_preview'),
    path('firma_image_preview/<int:id>/', utils.firma_image_preview, name='firma_image_preview'),
    path('rotate_image/', utils.firma_image_preview, name='firma_image_preview'),
    path('statistiche', views.statistiche, name='statistiche'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)