# Generated by Django 3.2.20 on 2024-04-08 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklists', '0007_checklistitem_original_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='checklist',
            name='archived',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='checklistitem',
            name='is_not_applicable',
            field=models.BooleanField(default=False, help_text='Not Applicable'),
        ),
    ]
