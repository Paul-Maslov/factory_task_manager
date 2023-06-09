# Generated by Django 4.1.7 on 2023-04-07 07:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("task_manager", "0008_alter_post_task"),
    ]

    operations = [
        migrations.AlterField(
            model_name="commentary",
            name="post",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="posts",
                to="task_manager.post",
            ),
        ),
    ]
