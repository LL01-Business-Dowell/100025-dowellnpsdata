from statistics import mode
from django.db import models

# Create your models here.
class QrCode(models.Model):
    logo = models.ImageField(upload_to='company-logo')
    brand_name = models.CharField(max_length=255)
    service = models.CharField(max_length=255)
    url = models.CharField(max_length=500)
    location = models.CharField(max_length=255)
    qr_code = models.FileField(upload_to='company-qrcode',blank= True)
    promotional_sentence = models.TextField(default=b'')
    image = models.BinaryField()
    event_id = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    privacy_policy_check = models.BooleanField(default=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    is_end = models.BooleanField(default=False)
    is_paused = models.BooleanField(default=False)
    reason = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return str(self.brand_name)
