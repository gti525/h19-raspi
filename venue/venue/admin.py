from django.contrib import admin, messages
from .models import Show, Venue, Ticket, Seller, ShowPublication


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


def publish_show(modeladmin, request, queryset):
    for show in queryset:
        for seller in Seller.objects.all():
            success, message = seller.create_show(show)
            if not success:
                messages.error(request, f'[{seller}] Erreur: {message}')
            else:
                messages.success(request, message)

def delete_from_seller(modeladmin, request, queryset):
    for show in queryset:
        for seller in Seller.objects.all():
            success, message = seller.create_show(show)
            if not success:
                messages.error(request, f'[{seller}] Erreur: {message}')
            else:
                messages.success(request, message)

def send_sale(modeladmin, request, queryset):
    for show in queryset:
        for seller in Seller.objects.all():
            success, message = seller.create_show(show)
            if not success:
                messages.error(request, f'[{seller}] Erreur: {message}')
            else:
                messages.success(request, message)

class ShowAdmin(admin.ModelAdmin):

    actions = (
        publish_show,
    )


admin.site.register(Show, ShowAdmin)
admin.site.register(Venue, VenueAdmin)
admin.site.register(Ticket)
admin.site.register(Seller)
admin.site.register(ShowPublication)
