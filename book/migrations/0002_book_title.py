# Generated by Django 4.2.3 on 2023-07-30 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("book", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="book",
            name="title",
            field=models.CharField(default="no title provided", max_length=250),
        ),
    ]