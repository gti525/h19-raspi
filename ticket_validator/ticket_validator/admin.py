from django.contrib import admin

from .models import ScanLog, Ticket


class ScanLogAdmin(admin.ModelAdmin):
    list_display = (
        'created',
        'ticket_uuid',
        'status',
    )


admin.site.register(ScanLog, ScanLogAdmin)
admin.site.register(Ticket)
