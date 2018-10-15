# Generated by Django 2.1.2 on 2018-10-12 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_entry', '0025_auto_20181009_0934'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataetl',
            name='district_name',
            field=models.CharField(default='Lusaka', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dataetl',
            name='province_name',
            field=models.CharField(default='Lusaka', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='activityreportform',
            name='quarter_been_reported',
            field=models.CharField(choices=[('201801', '1st Quarter-2018'), ('201802', '2nd Quarter-2018'), ('201803', '3rd Quarter-2018')], max_length=20, verbose_name='quarter being reported'),
        ),
    ]