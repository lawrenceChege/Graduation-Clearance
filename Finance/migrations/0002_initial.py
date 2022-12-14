# Generated by Django 4.1 on 2022-08-23 10:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('system_users', '0001_initial'),
        ('base', '0001_initial'),
        ('Finance', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentfee',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system_users.suser'),
        ),
        migrations.AddField(
            model_name='fee',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.state'),
        ),
    ]
