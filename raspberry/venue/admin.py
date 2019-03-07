from django.contrib import admin
from .models import Billet




class VenueAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'address',
        'capacity',
    )

    search_fields = (
        'name',
    )

    



admin.site.register(Billet)

