# Generated by Django 4.2.5 on 2023-09-27 18:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_number', models.BigIntegerField(primary_key=True, serialize=False)),
                ('gds_pnr', models.CharField(max_length=255)),
                ('supplier_pnr', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('STATUS_BOOK', 'B'), ('STATUS_TICKET', 'T'), ('STATUS_VOID', 'V'), ('STATUS_REFUND', 'R'), ('STATUS_BOOK_ERROR', 'E'), ('STATUS_TICKET_ERROR', 'C'), ('STATUS_PAID_WAIT', 'O'), ('STATUS_IN_PROGRESS', 'G'), ('STATUS_VOID_ERROR', 'W'), ('STATUS_REFUND_ERROR', 'F')], default='STATUS_BOOK', max_length=255)),
                ('created_at', models.DateTimeField()),
                ('ticket_time_limit', models.DateTimeField(blank=True, null=True)),
                ('void_time_limit', models.IntegerField(blank=True, null=True)),
                ('price_info', models.JSONField()),
                ('currency', models.CharField(max_length=255)),
                ('fare', models.JSONField()),
                ('provider', models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='Passenger',
            fields=[
                ('passenger_id', models.UUIDField(primary_key=True, serialize=False)),
                ('firstname', models.CharField(max_length=255)),
                ('lastname', models.CharField(max_length=255)),
                ('middlename', models.CharField(max_length=255)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')])),
                ('birth_date', models.DateField()),
                ('passenger_category', models.CharField(choices=[('ADT', 'ADT'), ('CHD', 'CHD'), ('INF', 'INF'), ('INS', 'INS')])),
                ('passenger_type', models.CharField(choices=[('Citizen', 'Citizen'), ('Student', 'Student'), ('Disabled', 'Disabled'), ('Pensioner', 'Pensioner')])),
                ('phone_number', models.CharField(max_length=255)),
                ('email_address', models.CharField(max_length=255)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='passenger', to='orders.order')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price_info', models.JSONField()),
                ('fares_info', models.JSONField()),
                ('baggage_info', models.JSONField()),
                ('passenger', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='ticket_info', to='orders.passenger')),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('passport_number', models.CharField(max_length=255)),
                ('passport_expiry', models.DateField()),
                ('nationality', models.CharField(max_length=255)),
                ('document_type', models.CharField(max_length=300)),
                ('passenger', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='document', to='orders.passenger')),
            ],
        ),
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agent_id', models.UUIDField()),
                ('agent_name', models.CharField(max_length=300)),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='agent', to='orders.order')),
            ],
        ),
    ]
