# Generated by Django 2.1.4 on 2019-01-12 03:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20190112_1039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='lanmus',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.Lanmus'),
        ),
    ]
