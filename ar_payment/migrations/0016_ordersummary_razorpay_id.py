# Generated by Django 5.1.3 on 2025-01-10 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ar_payment', '0015_alter_shippingaddress_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordersummary',
            name='razorpay_id',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]
