# Generated by Django 3.1.7 on 2021-03-21 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visits', models.PositiveIntegerField(default=0)),
                ('date', models.DateField(auto_now=True)),
            ],
        ),
    ]
