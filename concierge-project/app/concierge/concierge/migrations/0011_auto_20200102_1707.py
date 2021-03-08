# Generated by Django 3.0.1 on 2020-01-02 17:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('concierge', '0010_auto_20200101_2228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keytransfer',
            name='person_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='concierge.Person'),
        ),
        migrations.AlterField(
            model_name='keytransfer',
            name='room_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='concierge.Room'),
        ),
    ]