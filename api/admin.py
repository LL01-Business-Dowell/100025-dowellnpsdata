from django.contrib import admin


from api.models import QrCode


@admin.register(QrCode)
class QrCodeAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'brand_name', 'service', 'start_date', 'end_date',
        'privacy_policy_check', 'name', 'email',
    ]
