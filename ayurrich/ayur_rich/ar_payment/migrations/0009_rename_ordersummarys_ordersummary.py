# Generated by Django 5.1.3 on 2024-12-11 13:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ar_payment', '0008_ordersummarys_delete_ordersummary'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='OrderSummarys',
            new_name='OrderSummary',
        ),
    ]
