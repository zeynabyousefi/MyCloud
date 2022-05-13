# Generated by Django 4.0.4 on 2022-05-05 19:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('file', '0002_permissionuser_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='permissionuser',
            name='directory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='file.directorymodel'),
        ),
        migrations.AlterField(
            model_name='permissionuser',
            name='file',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='file.file'),
        ),
    ]
