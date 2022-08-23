# Generated by Django 4.1 on 2022-08-23 08:11

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='State',
            fields=[
                ('synced', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=35)),
                ('description', models.TextField(blank=True, max_length=255, null=True)),
            ],
            options={
                'ordering': ('name',),
                'unique_together': {('name',)},
            },
        ),
    ]
