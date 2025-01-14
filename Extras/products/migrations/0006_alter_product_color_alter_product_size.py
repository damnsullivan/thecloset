# Generated by Django 5.1.2 on 2024-10-27 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_product_gender_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='color',
            field=models.CharField(choices=[('Red', 'Vermelho'), ('Blue', 'Azul'), ('Green', 'Verde'), ('Black', 'Preto'), ('White', 'Branco'), ('Yellow', 'Amarelo')], default='Black', max_length=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='size',
            field=models.CharField(choices=[('XS', 'PP'), ('S', 'P'), ('M', 'M'), ('L', 'G'), ('XL', 'GG')], default='M', max_length=2),
        ),
    ]
