# Generated by Django 5.1.3 on 2024-12-07 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="fitness_goal",
            field=models.CharField(
                blank=True,
                choices=[
                    ("weight_loss", "Weight Loss"),
                    ("muscle_gain", "Muscle Gain"),
                    ("maintenance", "Body Maintenance"),
                    ("diebetic", "Diet Supervission"),
                ],
                max_length=20,
                null=True,
            ),
        ),
    ]
