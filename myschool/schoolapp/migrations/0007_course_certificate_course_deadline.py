# Generated by Django 5.0.4 on 2024-05-08 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schoolapp', '0006_language_course_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='Certificate',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='Deadline',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
