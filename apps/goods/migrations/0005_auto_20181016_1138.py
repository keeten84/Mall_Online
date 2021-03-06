# Generated by Django 2.1 on 2018-10-16 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0004_auto_20181016_0157'),
    ]

    operations = [
        migrations.RenameField(
            model_name='goods',
            old_name='shop_price',
            new_name='sale_price',
        ),
        migrations.AlterField(
            model_name='goodscategorybrand',
            name='image',
            field=models.ImageField(max_length=200, upload_to='brands/', verbose_name='品牌logo'),
        ),
    ]
