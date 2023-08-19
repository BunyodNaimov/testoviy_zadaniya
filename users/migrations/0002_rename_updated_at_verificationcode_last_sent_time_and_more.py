# Generated by Django 4.2.2 on 2023-08-19 08:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='verificationcode',
            old_name='updated_at',
            new_name='last_sent_time',
        ),
        migrations.AlterUniqueTogether(
            name='verificationcode',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='verificationcode',
            name='phone',
            field=models.CharField(max_length=15, null=True, unique=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')]),
        ),
        migrations.AlterField(
            model_name='verificationcode',
            name='code',
            field=models.CharField(max_length=6),
        ),
        migrations.AlterField(
            model_name='verificationcode',
            name='expired_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='verificationcode',
            name='verification_type',
            field=models.CharField(choices=[('register', 'Register'), ('login', 'Login')], max_length=50),
        ),
        migrations.AlterUniqueTogether(
            name='verificationcode',
            unique_together={('phone', 'verification_type')},
        ),
        migrations.RemoveField(
            model_name='verificationcode',
            name='attempts',
        ),
        migrations.RemoveField(
            model_name='verificationcode',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='verificationcode',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='verificationcode',
            name='signature',
        ),
    ]