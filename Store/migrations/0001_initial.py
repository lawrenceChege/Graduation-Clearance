# Generated by Django 4.1 on 2022-08-23 10:37

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0001_initial'),
        ('Finance', '0001_initial'),
        ('Faculty', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BorrowedGown',
            fields=[
                ('synced', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('borrow_date', models.DateField(auto_now=True)),
                ('return_date', models.DateField(auto_now=True)),
                ('penalty', models.DecimalField(blank=True, decimal_places=2, max_digits=25, null=True)),
                ('balance', models.DecimalField(blank=True, decimal_places=2, max_digits=25, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GraduationGown',
            fields=[
                ('synced', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('purchasing_date', models.DateField(auto_now=True)),
                ('size', models.TextField(max_length=3)),
                ('fee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Finance.fee')),
                ('programme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Faculty.programme')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.state')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BorrowedGownPenalty',
            fields=[
                ('synced', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('penalty', models.DecimalField(blank=True, decimal_places=2, max_digits=25, null=True)),
                ('balance', models.DecimalField(blank=True, decimal_places=2, max_digits=25, null=True)),
                ('gown', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Store.graduationgown')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.state')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
