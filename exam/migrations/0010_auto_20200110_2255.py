# Generated by Django 2.2.7 on 2020-01-11 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0009_auto_20200110_2252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='cover',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='images/'),
        ),
    ]
