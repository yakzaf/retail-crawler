# Generated by Django 2.2.5 on 2019-09-28 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HmTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('item_link', models.CharField(max_length=200)),
                ('image_source', models.CharField(max_length=300)),
                ('regular_price', models.FloatField()),
                ('sale_price', models.FloatField()),
            ],
        ),
    ]
