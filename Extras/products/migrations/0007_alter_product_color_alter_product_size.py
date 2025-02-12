# Generated by Django 5.1.2 on 2024-11-03 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_alter_product_color_alter_product_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='color',
            field=models.CharField(choices=[('Red', 'Vermelho'), ('Blue', 'Azul'), ('Green', 'Verde'), ('Black', 'Preto'), ('White', 'Branco'), ('Yellow', 'Amarelo'), ('Grey', 'Cinza'), ('Orange', 'Laranja'), ('Pink', 'Rosa'), ('Purple', 'Roxo')], default='Black', max_length=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='size',
            field=models.CharField(choices=[('XS', 'PP'), ('S', 'P'), ('M', 'M'), ('L', 'G'), ('XL', 'GG'), ('34', '34'), ('35', '35'), ('36', '36'), ('37', '37'), ('38', '38'), ('39', '39'), ('40', '40'), ('41', '41'), ('42', '42'), ('43', '43'), ('44', '44')], default='M', max_length=2),
        ),
    ]
