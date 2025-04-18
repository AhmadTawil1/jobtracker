# Generated by Django 5.2 on 2025-04-18 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0003_jobapplication_due_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobapplication',
            name='due_date',
            field=models.DateField(blank=True, help_text='The last day to apply for this position (optional)', null=True),
        ),
    ]
