# Generated by Django 2.1 on 2018-10-31 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0008_auto_20181031_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goodscategory',
            name='category_type',
            field=models.CharField(choices=[(1, '一级类目'), (2, '二级类目'), (3, '三级类目')], help_text='类目级别', max_length=10, verbose_name='类目级别'),
        ),
    ]
