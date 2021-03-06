# Generated by Django 2.2.7 on 2020-01-11 07:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0010_auto_20200110_2255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='cover',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='images/questions/'),
        ),
        migrations.CreateModel(
            name='ChoiceImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_cover', models.ImageField(blank=True, default=None, null=True, upload_to='images/choices/')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam.Question')),
            ],
        ),
    ]
