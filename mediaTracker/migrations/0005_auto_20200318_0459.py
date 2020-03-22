# Generated by Django 3.0.4 on 2020-03-18 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mediaTracker', '0004_auto_20200313_0233'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='author1',
            new_name='author',
        ),
        migrations.RemoveField(
            model_name='book',
            name='author2',
        ),
        migrations.RemoveField(
            model_name='book',
            name='isInPrint',
        ),
        migrations.RemoveField(
            model_name='book',
            name='seriesName',
        ),
        migrations.RemoveField(
            model_name='book',
            name='seriesNum',
        ),
        migrations.AddField(
            model_name='book',
            name='publisher',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
