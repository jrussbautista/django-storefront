# Generated by Django 4.0.6 on 2022-09-14 15:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_alter_customer_options_remove_customer_email_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'permissions': [('cancel_order', 'Can cancel order')]},
        ),
    ]
