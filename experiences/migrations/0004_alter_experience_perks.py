# Generated by Django 4.0.8 on 2022-12-19 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiences', '0003_alter_experience_category_alter_experience_host'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experience',
            name='perks',
            field=models.ManyToManyField(blank=True, to='experiences.perk'),
        ),
    ]
