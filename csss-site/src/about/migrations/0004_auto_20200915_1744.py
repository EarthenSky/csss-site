# Generated by Django 2.2.13 on 2020-09-15 17:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('about', '0003_auto_20200720_1953'),
    ]

    operations = [
        migrations.CreateModel(
            name='OfficerEmailListAndPositionMapping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('term_position_number', models.IntegerField(default=0)),
                ('officer_position', models.CharField(default='President', max_length=300)),
                ('email', models.CharField(default='NA', max_length=140)),
                ('marked_for_deletion', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='officer',
            name='sfu_email_alias',
            field=models.CharField(default='NA', max_length=140),
        ),
        migrations.AddField(
            model_name='officer',
            name='sfu_officer_mailing_list_email',
            field=models.CharField(default='NA', max_length=140),
        ),
        migrations.AddField(
            model_name='officer',
            name='start_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
