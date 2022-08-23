# Generated by Django 4.1 on 2022-08-23 08:11

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0001_initial'),
        ('system_users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fee',
            fields=[
                ('synced', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=35)),
                ('description', models.TextField(blank=True, max_length=255, null=True)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=25)),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.state')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StudentFee',
            fields=[
                ('synced', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('amount_paid', models.DecimalField(decimal_places=2, default=0.0, max_digits=25)),
                ('balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=25)),
                ('fee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Finance.fee')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system_users.suser')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StudentFeePayment',
            fields=[
                ('synced', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=25)),
                ('receipt', models.TextField(blank=True, max_length=50, null=True)),
                ('student_fee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Finance.studentfee')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]