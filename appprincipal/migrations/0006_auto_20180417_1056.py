# Generated by Django 2.0.4 on 2018-04-17 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appprincipal', '0005_curso'),
    ]

    operations = [
        migrations.AlterField(
            model_name='curso',
            name='codigo',
            field=models.CharField(max_length=10, primary_key=True, serialize=False),
        ),
    ]
