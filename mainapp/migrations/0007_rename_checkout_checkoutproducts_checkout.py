# Generated by Django 4.1.7 on 2023-07-13 10:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0006_buyer_otp'),
    ]

    operations = [
        migrations.RenameField(
            model_name='checkoutproducts',
            old_name='checkout',
            new_name='Checkout',
        ),
    ]
