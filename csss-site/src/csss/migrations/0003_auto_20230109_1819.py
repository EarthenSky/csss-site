# Generated by Django 2.2.27 on 2023-01-09 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csss', '0002_error'),
    ]

    operations = [
        migrations.CreateModel(
            name='CSSSError',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=500)),
                ('message', models.CharField(max_length=5000)),
                ('processed', models.BooleanField(default=False)),
            ],
        ),
        migrations.DeleteModel(
            name='Error',
        ),
    ]