# Generated by Django 5.0.3 on 2024-07-08 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_rename_costumer_customer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='proudct',
            name='is_sale',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='proudct',
            name='sale_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
    ]
