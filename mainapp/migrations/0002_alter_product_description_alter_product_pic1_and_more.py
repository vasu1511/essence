# Generated by Django 4.1.7 on 2023-04-05 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(default='THIS IS SAMPLE PRODUCT'),
        ),
        migrations.AlterField(
            model_name='product',
            name='pic1',
            field=models.ImageField(upload_to='product'),
        ),
        migrations.AlterField(
            model_name='product',
            name='pic2',
            field=models.ImageField(upload_to='product'),
        ),
    ]
