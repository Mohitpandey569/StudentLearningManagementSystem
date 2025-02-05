# Generated by Django 5.0.4 on 2024-05-11 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schoolapp', '0011_payment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='state',
            new_name='status',
        ),
        migrations.RenameField(
            model_name='payment',
            old_name='usercourse',
            new_name='user_course',
        ),
        migrations.AlterField(
            model_name='payment',
            name='data',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='order_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
