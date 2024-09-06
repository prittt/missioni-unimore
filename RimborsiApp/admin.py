from django.contrib import admin

from .models import *


# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Profile._meta.fields]
    list_display.append('cf')


class IndirizzoAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Indirizzo._meta.fields]


class AutomobileAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Automobile._meta.fields]


class MissioneAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Missione._meta.fields]
    list_display.append('durata_gg')
    list_display.append('data_richiesta')


class CategoriaAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Categoria._meta.fields]


class StatoAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Stato._meta.fields]


class TrasportoAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Trasporto._meta.fields]


class DateRichiestaAdmin(admin.ModelAdmin):
    list_display = [f.name for f in ModuliMissione._meta.fields]


class SpesaAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Spesa._meta.fields]


class SpesaMissioneAdmin(admin.ModelAdmin):
    list_display = [f.name for f in SpesaMissione._meta.fields]


class PastiAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Pasti._meta.fields]


admin_site = admin.site

admin_site.register(Profile, ProfileAdmin)
admin_site.register(Automobile, AutomobileAdmin)
admin_site.register(Missione, MissioneAdmin)
admin_site.register(Indirizzo, IndirizzoAdmin)
admin_site.register(Categoria, CategoriaAdmin)
admin_site.register(Stato, StatoAdmin)
admin_site.register(Trasporto, TrasportoAdmin)
admin_site.register(ModuliMissione, DateRichiestaAdmin)
admin.site.register(Spesa, SpesaAdmin)
admin.site.register(SpesaMissione, SpesaMissioneAdmin)
admin_site.register(Pasti, PastiAdmin)