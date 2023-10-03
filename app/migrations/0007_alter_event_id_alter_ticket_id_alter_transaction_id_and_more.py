# Generated by Django 4.1.7 on 2023-08-22 14:56

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_event_id_alter_ticket_id_alter_transaction_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='id',
            field=models.UUIDField(default=uuid.UUID('6f4162db-335a-4105-8737-274716f1cf05'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='id',
            field=models.UUIDField(default=uuid.UUID('e395d85a-2637-4418-aecd-cb2414ad56ed'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='id',
            field=models.UUIDField(default=uuid.UUID('815b879b-3f37-4f22-a732-0271e5bf3a85'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='venue',
            name='id',
            field=models.UUIDField(default=uuid.UUID('dc79f00f-4ec3-4a79-8e56-69e8aeb55db0'), editable=False, primary_key=True, serialize=False),
        ),
    ]
