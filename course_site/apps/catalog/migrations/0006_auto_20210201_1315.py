# Generated by Django 3.1.5 on 2021-02-01 13:15

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0005_auto_20210201_1059'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Book',
            new_name='Course',
        ),
        migrations.AlterField(
            model_name='language',
            name='name',
            field=models.CharField(help_text="Enter the coursec's natural language (e.g. English, French, Japanese etc.)", max_length=200),
        ),
    ]
