# Generated by Django 2.0.4 on 2018-10-05 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_entry', '0023_auto_20180911_1440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dacavalidation',
            name='validation_status',
            field=models.CharField(choices=[('needs_review', 'Needs Review'), ('approved', 'Approved')], max_length=15, verbose_name='DACA validation status'),
        ),
        migrations.AlterField(
            model_name='dataetl',
            name='value',
            field=models.DecimalField(decimal_places=5, max_digits=20),
        ),
        migrations.AlterField(
            model_name='pitmeovalidation',
            name='validation_status',
            field=models.CharField(choices=[('needs_review', 'Needs Review'), ('approved', 'Approved')], max_length=15, verbose_name='PITMEO validation status'),
        ),
    ]
