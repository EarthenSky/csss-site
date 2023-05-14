# Generated by Django 2.2.27 on 2023-04-12 01:42

import csss.PSTDateTimeField
from django.db import migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('resource_management', '0018_googledrivefileawaitingownershipchange'),
    ]

    operations = [
        migrations.AlterField(
            model_name='googledrivefileawaitingownershipchange',
            name='latest_date_check',
            field=csss.PSTDateTimeField.PSTDateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='googledriverootfolderbadaccess',
            name='latest_date_check',
            field=csss.PSTDateTimeField.PSTDateTimeField(default=django.utils.timezone.now),
        ),
    ]