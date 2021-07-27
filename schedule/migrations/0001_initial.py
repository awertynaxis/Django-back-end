# Generated by Django 3.2.5 on 2021-07-21 14:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('order', '0001_initial'),
        ('master', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_slot', models.DateTimeField()),
                ('master', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedule', to='master.master')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order', to='order.order')),
            ],
        ),
    ]
