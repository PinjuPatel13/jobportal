# Generated by Django 5.1.6 on 2025-03-01 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0009_studentuser_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='recruiter',
            name='email',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
