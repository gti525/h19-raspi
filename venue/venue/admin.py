from django.contrib import admin, messages
from .models import Show, Venue, Ticket, Seller, ShowPublication
from .models import TicketValidator

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

    def sold(self, object):
        tickets = object.get_tickets()
        sold = tickets.filter(sold=True).count()

        return f'{round(sold/tickets.count(), 2)*100}% ({sold})'

    list_display = (
        'name',
        'sold',
    )


admin.site.register(Show, ShowAdmin)
admin.site.register(Venue, VenueAdmin)
admin.site.register(Ticket)
admin.site.register(Seller)
admin.site.register(ShowPublication)
admin.site.register(TicketValidator)
