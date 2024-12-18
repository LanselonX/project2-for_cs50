# Generated by Django 5.1.4 on 2024-12-18 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuctionList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='title')),
                ('description', models.TextField(verbose_name='description')),
                ('start_price', models.DecimalField(decimal_places=2, max_digits=2, verbose_name='start_price')),
            ],
        ),
    ]