# Generated by Django 2.2.27 on 2023-02-01 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elections', '0012_auto_20220812_2203'),
    ]

    operations = [
        migrations.AddField(
            model_name='nominee',
            name='instagram',
            field=models.CharField(default='NONE', max_length=300, verbose_name='Instagram Link'),
        ),
    ]
