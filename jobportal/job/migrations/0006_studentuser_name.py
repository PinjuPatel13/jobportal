# Generated by Django 5.1.6 on 2025-02-27 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0005_studentuser_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentuser',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
