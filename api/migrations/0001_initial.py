# Generated by Django 4.0.4 on 2023-12-05 21:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='QrCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo', models.ImageField(upload_to='company-logo')),
                ('brand_name', models.CharField(max_length=255)),
                ('service', models.CharField(max_length=255)),
                ('url', models.CharField(max_length=500)),
                ('country', models.TextField(max_length=255)),
                ('region', models.TextField(default=b'', max_length=255)),
                ('qr_code', models.FileField(blank=True, upload_to='company-qrcode')),
                ('promotional_sentence', models.TextField(default=b'')),
                ('image', models.BinaryField()),
                ('event_id', models.CharField(blank=True, max_length=255, null=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('privacy_policy_check', models.BooleanField(default=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(blank=True, max_length=255, null=True)),
                ('username', models.CharField(blank=True, max_length=255, null=True)),
                ('is_end', models.BooleanField(default=False)),
                ('is_paused', models.BooleanField(default=False)),
                ('reason', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='QrCodeV2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo', models.ImageField(upload_to='company-logo')),
                ('brand_name', models.CharField(max_length=255)),
                ('service', models.TextField(max_length=255)),
                ('url', models.CharField(max_length=500)),
                ('country', models.TextField(max_length=255)),
                ('region', models.TextField(default=b'', max_length=255)),
                ('qr_code', models.FileField(blank=True, upload_to='company-qrcode')),
                ('promotional_sentence', models.TextField(default=b'')),
                ('image', models.BinaryField()),
                ('event_id', models.CharField(blank=True, max_length=255, null=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('privacy_policy_check', models.BooleanField(default=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(blank=True, max_length=255, null=True)),
                ('username', models.CharField(blank=True, max_length=255, null=True)),
                ('is_end', models.BooleanField(default=False)),
                ('is_paused', models.BooleanField(default=False)),
                ('reason', models.CharField(blank=True, max_length=500, null=True)),
                ('link', models.CharField(blank=True, max_length=500, null=True)),
                ('participantsLimit', models.JSONField(blank=True, default=dict, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SurveyCoordinator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('participants', models.JSONField(blank=True, default=dict, null=True)),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.qrcodev2')),
            ],
        ),
    ]
