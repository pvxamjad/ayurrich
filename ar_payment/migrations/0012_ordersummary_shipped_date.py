# Generated by Django 5.1.3 on 2024-12-14 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ar_payment', '0011_ordersummary_orderd_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordersummary',
            name='shipped_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
