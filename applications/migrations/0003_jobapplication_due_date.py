# Generated by Django 5.2 on 2025-04-18 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0002_jobapplication_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobapplication',
            name='due_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
