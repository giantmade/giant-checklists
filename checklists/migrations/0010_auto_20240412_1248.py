# Generated by Django 3.2.20 on 2024-04-12 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklists', '0009_auto_20240315_0832'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AddField(
            model_name='checklist',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]