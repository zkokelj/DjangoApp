# Generated by Django 4.0.3 on 2022-07-14 06:50

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organizations', '0008_alter_organization_mobile_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalOrganization',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200)),
                ('address', models.CharField(max_length=200)),
                ('tax_number', models.CharField(max_length=8, validators=[django.core.validators.RegexValidator('^[0-9]{8}$')])),
                ('mobile_number', models.CharField(max_length=13, null=True, validators=[django.core.validators.RegexValidator('00|\\+386[0-9]{8}')])),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical organization',
                'verbose_name_plural': 'historical organizations',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]