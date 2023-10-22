# Generated by Django 4.2.6 on 2023-10-22 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autocards_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='deck',
            name='cards',
            field=models.ManyToManyField(to='autocards_app.card'),
        ),
        migrations.AddField(
            model_name='deck',
            name='name',
            field=models.TextField(default='n'),
            preserve_default=False,
        ),
    ]
