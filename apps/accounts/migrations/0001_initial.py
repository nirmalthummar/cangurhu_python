# Generated by Django 3.2.13 on 2022-05-25 06:14

import core.utils
from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django_otp.util


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('snippets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('has_email_verified', models.BooleanField(default=False)),
                ('has_mobile_verified', models.BooleanField(default=False)),
                ('user_id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('username', models.CharField(blank=True, max_length=50)),
                ('email', models.EmailField(db_index=True, max_length=254, unique=True)),
                ('isd_code', models.CharField(help_text='Country ISD Code', max_length=20)),
                ('mobile_number', models.CharField(db_index=True, max_length=16, unique=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=False, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('role', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('customer', 'Customer'), ('courier', 'Courier'), ('cook', 'Cook')], max_length=12), blank=True, default=list, size=None)),
                ('dob', models.DateField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('status', models.IntegerField(choices=[(1, 'Active'), (0, 'Inactive'), (2, 'Delete')], default=1)),
                ('country_id', models.ForeignKey(blank=True, db_column='country_id', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='country', to='snippets.country')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'User Management',
                'db_table': 'table_user_account',
            },
        ),
        migrations.CreateModel(
            name='VerificationDevice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The human-readable name of this device.', max_length=64)),
                ('confirmed', models.BooleanField(default=True, help_text='Is this device ready for use?')),
                ('mobile_number', models.CharField(max_length=16, unique=True)),
                ('secret_key', models.CharField(default=core.utils.default_key, help_text='Hex-encoded secret key to generate totp tokens.', max_length=40, unique=True, validators=[django_otp.util.hex_validator])),
                ('last_verified_counter', models.BigIntegerField(default=-1, help_text='The counter value of the latest verified token.The next token must be at a higher counter value.It makes sure a token is used only once.')),
                ('verified', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='devices', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Verification Device',
                'abstract': False,
            },
        ),
    ]
