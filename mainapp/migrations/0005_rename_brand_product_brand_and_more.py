# Generated by Django 4.1.7 on 2023-07-08 15:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_contactus_checkoutproducts_pid_wishlist'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='brand',
            new_name='Brand',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='maincategory',
            new_name='Maincategory',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='subcategory',
            new_name='Subcategory',
        ),
    ]
