# Generated by Django 4.0.3 on 2022-07-10 08:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Organizations',
            new_name='Organization',
        ),
    ]
