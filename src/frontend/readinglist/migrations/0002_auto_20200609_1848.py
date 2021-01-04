# Generated by Django 2.2.11 on 2020-06-09 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('readinglist', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='paper',
            old_name='metadata',
            new_name='_metadata',
        ),
        migrations.AlterField(
            model_name='paper',
            name='_metadata',
            field=models.TextField(db_column='metadata'),
        ),
        migrations.AlterUniqueTogether(
            name='paper',
            unique_together={('source', 'handle')},
        ),
    ]