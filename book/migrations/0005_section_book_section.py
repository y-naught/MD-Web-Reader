# Generated by Django 4.2.3 on 2023-08-10 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("book", "0004_section_section_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="section",
            name="book_section",
            field=models.CharField(
                choices=[
                    ("A", "System Basics with Rhino"),
                    ("B", "Parametric Design with Python and Grasshopper"),
                    ("C", "Computational Design Methods"),
                ],
                default="A",
                max_length=2,
            ),
        ),
    ]