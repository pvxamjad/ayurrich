# Generated by Django 5.1.3 on 2024-12-16 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ar_payment', '0013_alter_ordersummary_orderd_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingaddress',
            name='country',
            field=models.CharField(blank=True, default='India', max_length=255, null=True),
        ),
    ]
