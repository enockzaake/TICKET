# Generated by Django 4.1.7 on 2023-08-21 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_ticket_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='quantity_bought',
            field=models.IntegerField(default=0),
        ),
    ]