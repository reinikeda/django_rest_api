# Generated by Django 4.1.7 on 2023-03-07 06:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('playlist', '0003_rename_band_id_album_band_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='band',
            old_name='band',
            new_name='name',
        ),
    ]