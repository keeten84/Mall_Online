# Generated by Django 2.1 on 2018-11-08 14:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0002_auto_20181016_0157'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shoppingcart',
            old_name='goods_nums',
            new_name='nums',
        ),
    ]
