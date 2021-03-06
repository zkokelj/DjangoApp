# Generated by Django 4.0.3 on 2022-07-13 22:45

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0007_organization_mobile_number_alter_organization_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='mobile_number',
            field=models.CharField(max_length=13, null=True, validators=[django.core.validators.RegexValidator('00|\\+386[0-9]{8}')]),
        ),
    ]
