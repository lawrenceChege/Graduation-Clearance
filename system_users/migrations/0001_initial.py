# Generated by Django 4.1 on 2022-08-23 08:11

import base.models
from django.db import migrations, models
import django.db.models.deletion
import system_users.backend.managers
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtendedSUserPermission',
            fields=[
                ('synced', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Extended Permission',
                'verbose_name_plural': 'Extended Permissions',
            },
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('synced', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=35)),
                ('description', models.TextField(blank=True, max_length=255, null=True)),
                ('simple_name', models.TextField(blank=True, max_length=255, null=True)),
                ('extendable', models.BooleanField(default=False)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='system_users.permission')),
                ('state', models.ForeignKey(default=base.models.State.default_state, on_delete=django.db.models.deletion.CASCADE, to='base.state')),
            ],
            options={
                'unique_together': {('name',)},
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('synced', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=35)),
                ('description', models.TextField(blank=True, max_length=255, null=True)),
                ('is_staff_role', models.BooleanField(default=False)),
                ('is_super_admin_role', models.BooleanField(default=False)),
                ('state', models.ForeignKey(default=base.models.State.default_state, on_delete=django.db.models.deletion.CASCADE, to='base.state')),
            ],
            options={
                'unique_together': {('name',)},
            },
        ),
        migrations.CreateModel(
            name='SUser',
            fields=[
                ('synced', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(help_text='System-wide identifier used to identify the admin for authentication', max_length=50, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('phone_number', models.CharField(max_length=20, verbose_name='phone number')),
                ('email', models.CharField(max_length=50)),
                ('is_active', models.BooleanField(default=True, help_text='User is currently active.', verbose_name='active')),
                ('is_staff', models.BooleanField(default=False, help_text='User can login login to the dashboard.', verbose_name='staff')),
                ('is_superuser', models.BooleanField(default=False, help_text='User has full permissions on the admin dashboard.', verbose_name='super user')),
                ('last_activity', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='last activity')),
                ('permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='SUser_set', related_query_name='SUser', through='system_users.ExtendedSUserPermission', to='system_users.permission')),
                ('role', models.ForeignKey(blank=True, help_text='The role for the user belongs to. Cannot be null unless super user', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='roles', to='system_users.role')),
                ('state', models.ForeignKey(default=base.models.State.default_state, on_delete=django.db.models.deletion.CASCADE, to='base.state')),
            ],
            options={
                'abstract': False,
                'unique_together': {('id',)},
            },
            managers=[
                ('objects', system_users.backend.managers.SUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='SUserSecurityQuestion',
            fields=[
                ('synced', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('security_question', models.TextField(max_length=50)),
                ('answer_hash', models.CharField(max_length=255)),
                ('SUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_questions', to='system_users.suser')),
                ('state', models.ForeignKey(default=base.models.State.default_state, on_delete=django.db.models.deletion.CASCADE, to='base.state')),
            ],
            options={
                'ordering': ('-date_created',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SUserPassword',
            fields=[
                ('synced', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('hashed_password', models.BooleanField(default=False, editable=False, verbose_name='is password hashed')),
                ('SUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_passwords', to='system_users.suser')),
                ('state', models.ForeignKey(default=base.models.State.default_state, on_delete=django.db.models.deletion.CASCADE, to='base.state')),
            ],
            options={
                'verbose_name': 'Password',
                'verbose_name_plural': 'Passwords',
                'ordering': ('-date_created',),
            },
        ),
        migrations.AddField(
            model_name='extendedsuserpermission',
            name='SUser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system_users.suser'),
        ),
        migrations.AddField(
            model_name='extendedsuserpermission',
            name='permission',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system_users.permission'),
        ),
        migrations.AddField(
            model_name='extendedsuserpermission',
            name='state',
            field=models.ForeignKey(default=base.models.State.default_state, on_delete=django.db.models.deletion.CASCADE, to='base.state'),
        ),
        migrations.CreateModel(
            name='RolePermission',
            fields=[
                ('synced', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('permission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system_users.permission')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system_users.role')),
                ('state', models.ForeignKey(default=base.models.State.default_state, on_delete=django.db.models.deletion.CASCADE, to='base.state')),
            ],
            options={
                'unique_together': {('role', 'permission')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='extendedsuserpermission',
            unique_together={('SUser', 'permission')},
        ),
    ]