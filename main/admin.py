from django.contrib import admin
from .models import Igrica, Kupac

# Register the Igrica model
class IgricaAdmin(admin.ModelAdmin):
    list_display = ('igrica_naslov', 'igrica_vrijeme_objave')
    search_fields = ('igrica_naslov',)
    list_filter = ('igrica_vrijeme_objave',)

# Register the Kupac model
class KupacAdmin(admin.ModelAdmin):
    list_display = ('kupac_ime', 'kupac_prezime', 'kupac_broj_mobitela')
    search_fields = ('kupac_ime', 'kupac_prezime')
    filter_horizontal = ('kupac_igrice',)  # Makes ManyToMany fields more user-friendly in the admin

# Register the models with their admin classes
admin.site.register(Igrica, IgricaAdmin)
# Register your models here.
