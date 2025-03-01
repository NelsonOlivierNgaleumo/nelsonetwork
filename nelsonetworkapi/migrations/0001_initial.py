# Generated by Django 4.2.17 on 2025-03-01 16:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('device_id', models.AutoField(primary_key=True, serialize=False)),
                ('device_name', models.CharField(max_length=100)),
                ('device_image', models.URLField()),
                ('age_of_device', models.CharField(max_length=50)),
                ('device_ip', models.GenericIPAddressField()),
                ('device_type', models.CharField(max_length=50)),
                ('device_description', models.CharField(max_length=200)),
                ('serial_number', models.CharField(max_length=100)),
                ('mac_address', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
                ('last_software_update', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Network',
            fields=[
                ('network_id', models.AutoField(primary_key=True, serialize=False)),
                ('network_name', models.CharField(max_length=100)),
                ('network_type', models.CharField(max_length=50)),
                ('number_of_staff', models.IntegerField()),
                ('setup_recommendation', models.CharField(max_length=200)),
                ('network_ip_address', models.GenericIPAddressField()),
                ('location', models.CharField(max_length=100)),
                ('device_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nelsonetworkapi.device')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('role', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='NetworkDevice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive'), ('Pending', 'Pending')], default='Pending', max_length=20)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='devicenetworks', to='nelsonetworkapi.device')),
                ('network', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='networkdevices', to='nelsonetworkapi.network')),
            ],
        ),
        migrations.AddField(
            model_name='network',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nelsonetworkapi.user'),
        ),
        migrations.CreateModel(
            name='Documentation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_type', models.CharField(max_length=50)),
                ('configuration', models.TextField()),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nelsonetworkapi.device')),
            ],
        ),
        migrations.AddField(
            model_name='device',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nelsonetworkapi.user'),
        ),
    ]
