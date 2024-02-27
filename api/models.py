from statistics import mode
from django.db import models
import ast

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
    participantsLimit = models.JSONField(null=True, blank=True, default=dict)
    category = models.CharField(max_length=500, null=True, blank=True)
    latitude = models.CharField(max_length=500, blank=True, null=True)
    longitude = models.CharField(max_length=500, blank=True, null=True)
    
    def save(self, *args, **kwargs):
       if self.pk is None:
            # Convert the participantsLimit string to a dictionary
            
            # participants_limit_values = self.participantsLimit[0].split(', ')  
            participants_limit_values = int(self.participantsLimit)
            print('participants ', participants_limit_values)
            # regions_values = self.region.split(', ')
            regions_values = self.region
            print('db regions ', regions_values)
            
            participants_limit_dict = {regions_values: participants_limit_values}
            print('its here ', participants_limit_dict)

            # Save the dictionary to the model
            # self.participantsLimit = participants_limit_dict
            
            # Create SurveyCoordinator when a new QrCodeV2 is saved
            super(QrCodeV2, self).save(*args, **kwargs)
            # self.link = f"{self.url}/{self.pk}"
            self.link = f'{self.link}?survey_id={self.pk}'

            survey_coordinator = SurveyCoordinator.objects.create(survey=self)
            survey_coordinator.participants = participants_limit_dict
            survey_coordinator.save()
       else:
           super(QrCodeV2, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.brand_name)
    
    
    
    

class SurveyCoordinator(models.Model):
    survey = models.ForeignKey(QrCodeV2, on_delete=models.CASCADE)
    participants = models.JSONField(null=True, blank=True, default=dict)
    
    
    def __str__(self):
        return self.survey.brand_name