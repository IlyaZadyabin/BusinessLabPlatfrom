# Generated by Django 3.1.5 on 2021-02-01 14:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_auto_20210201_1354'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='borrower',
            new_name='attendants',
        ),
    ]
