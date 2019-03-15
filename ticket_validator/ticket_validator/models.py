from django.db import models
from django.utils.translation import gettext as _


class ScanLog(models.Model):
    SCAN_STATUS = (
        ('OK', _('Scanné, OK')),
        ('FAIL', _('Déjà scanné! FAIL')),
    )

    created = models.DateTimeField(auto_now_add=True)
    ticket_uuid = models.UUIDField(editable=False)
    status = models.CharField(choices=SCAN_STATUS, max_length=4)

    def __str__(self):
        return self.ticket_uuid


class Ticket(models.Model):
    uuid = models.UUIDField(unique=True)
    show = models.UUIDField()
    scanned = models.BooleanField(default=False)

    def __str__(self):
        return self.uuid

    class Meta:
        unique_together = (
            ('uuid', 'show'),
        )
