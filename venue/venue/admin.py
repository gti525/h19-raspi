from django.contrib import admin
from .models import Show, Venue, Ticket


admin.site.register(Show)
admin.site.register(Venue)
admin.site.register(Ticket)
