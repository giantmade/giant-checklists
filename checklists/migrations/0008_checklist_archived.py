# Generated by Django 3.2.20 on 2023-11-11 12:37

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
    ]
