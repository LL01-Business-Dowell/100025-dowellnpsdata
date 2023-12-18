from django.contrib import admin


from .models import QrCode, QrCodeV2, SurveyCoordinator


@admin.register(QrCode)
class QrCodeAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'brand_name', 'service',  'start_date', 'end_date',
        'privacy_policy_check', 'name', 'email', 'is_end', 'reason'
    ]
    
    
@admin.register(QrCodeV2)
class QrCodeAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'brand_name', 'service', 'participantsLimit', 'start_date', 'end_date',
        'privacy_policy_check', 'name', 'email', 'is_end', 'reason'
    ]

admin.site.register(SurveyCoordinator)
# admin.site.register(QrCodeV2)