# Generated by Django 5.1.3 on 2024-12-05 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_calendarevent_notes_calendarevent_recipe_url_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendarevent',
            name='meal_type',
            field=models.CharField(blank=True, choices=[('lunch', 'Lunch'), ('dinner', 'Dinner')], default='lunch', max_length=10, null=True),
        ),
    ]
