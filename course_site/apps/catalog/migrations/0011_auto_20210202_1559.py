# Generated by Django 3.1.5 on 2021-02-02 15:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0010_auto_20210201_1627'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='imprint',
        ),
        migrations.RemoveField(
            model_name='course',
            name='isbn',
        ),
    ]