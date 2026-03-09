# Generated migration — adds face_data field to Customer and Seller models

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='face_data',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='seller',
            name='face_data',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
