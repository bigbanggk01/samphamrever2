# Generated by Django 4.0.4 on 2022-06-22 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_create_trigger'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_name',
            field=models.TextField(max_length=200),
        ),
    ]
