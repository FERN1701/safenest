# Generated by Django 5.0.4 on 2024-12-07 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barangay', '0004_remove_user_roles_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='middle',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
