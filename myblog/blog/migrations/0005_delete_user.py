# Generated by Django 2.1.4 on 2019-01-11 04:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]