
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


    


    def __str__(self):
        return str(self.brand_name)