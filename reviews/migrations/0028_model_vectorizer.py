# Generated by Django 4.1.7 on 2023-06-13 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0027_alter_model_model_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='model',
            name='vectorizer',
            field=models.FileField(null=True, upload_to='models/vect/'),
        ),
    ]
