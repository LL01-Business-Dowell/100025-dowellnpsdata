from statistics import mode
from django.db import models

# Create your models here.
class QrCode(models.Model):
    logo = models.ImageField(upload_to='company-logo')
    brand_name = models.CharField(max_length=255)
    service = models.CharField(max_length=255)
    url = models.CharField(max_length=500)
    country = models.TextField(max_length=255)
    region = models.TextField(max_length=255, default=b'')
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
    # link = models.CharField(max_length=500, blank=True, null=True)
    # participantsLimit = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.brand_name)
    
    
    
class QrCodeV2(models.Model):
    logo = models.ImageField(upload_to='company-logo')
    brand_name = models.CharField(max_length=255)
    service = models.TextField(max_length=255)
    url = models.CharField(max_length=500)
    country = models.TextField(max_length=255)
    region = models.TextField(max_length=255, default=b'')
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
    link = models.CharField(max_length=500, blank=True, null=True)
    participantsLimit = models.TextField(null=True, blank=True)
    
    
    def save(self, *args, **kwargs):
        if self.pk is None:
            super(QrCodeV2, self).save(*args, **kwargs)  
            self.link = f"{self.url}/{self.pk}"
        else:
            super(QrCodeV2, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.brand_name)
    
    
    

class SurveyCoordinator(models.Model):
    survey = models.ForeignKey(QrCodeV2, on_delete=models.CASCADE)
    participants = models.TextField()