import uuid
from django.db import models
from django.utils import timezone
from django.urls import reverse


class QRToken(models.Model):
    token = models.UUIDField(unique=True, editable=False)
    product_id = models.IntegerField()
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=255)
    image_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(blank=True, null=True)

    def is_valid(self):
        if self.expires_at:
            return timezone.now() <= self.expires_at
        return True

    def get_absolute_url(self):
        return reverse("qr_goods:product_by_token", args=[str(self.token)])

    def __str__(self):
        return f"QRToken({self.product_id})"
