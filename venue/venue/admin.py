from django.contrib import admin
from .models import Show, Venue, Ticket


class ShowInline(admin.StackedInline):
    model = Show
    extra = 0

class VenueAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'address',
        'capacity',
    )

    search_fields = (
        'name',
    )

    inlines = [
        ShowInline,
    ]



admin.site.register(Show)
admin.site.register(Venue, VenueAdmin)
admin.site.register(Ticket)
