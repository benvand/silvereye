# Generated by Django 2.2.14 on 2020-08-21 02:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('input', '0008_supplieddata_data_schema_version'),
    ]

    operations = [
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publisher_scheme', models.CharField(blank=True, default='', help_text='The scheme that holds the unique identifiers used to identify publishers', max_length=1024, null=True)),
                ('publisher_id', models.CharField(help_text='The unique ID for this publisher under the given ID scheme', max_length=1024, null=True)),
                ('publisher_name', models.CharField(help_text='The name of the organization or department responsible for publishing this data', max_length=1024, null=True)),
                ('uri', models.CharField(blank=True, default='', help_text='A URI to identify the publisher', max_length=1024, null=True)),
                ('ocid_prefix', models.CharField(blank=True, default='', help_text='OCID prefix registered by the publisher', max_length=11, null=True)),
                ('contact_name', models.CharField(blank=True, default='', max_length=1024, null=True)),
                ('contact_email', models.CharField(blank=True, default='', max_length=1024, null=True)),
                ('contact_telephone', models.CharField(blank=True, default='', max_length=1024, null=True)),
            ],
            options={
                'db_table': 'silvereye_publisher_metadata',
                'ordering': ['publisher_name'],
            },
        ),
        migrations.CreateModel(
            name='PublisherMetrics',
            fields=[
                ('publisher_id', models.CharField(max_length=1024, primary_key=True, serialize=False)),
                ('publisher_name', models.CharField(max_length=1024)),
                ('count_lastmonth', models.IntegerField(null=True)),
                ('count_last3months', models.IntegerField(null=True)),
                ('count_last12months', models.IntegerField(null=True)),
                ('average_lastmonth', models.IntegerField(null=True)),
                ('average_last3months', models.IntegerField(null=True)),
                ('average_last12months', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PublisherMonthlyCounts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(null=True)),
                ('count_tenders', models.IntegerField(null=True)),
                ('count_awards', models.IntegerField(null=True)),
                ('count_spend', models.IntegerField(null=True)),
                ('publisher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='silvereye.Publisher')),
            ],
        ),
        migrations.CreateModel(
            name='FileSubmission',
            fields=[
                ('supplied_data', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='input.SuppliedData')),
                ('publisher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='silvereye.Publisher')),
            ],
            bases=('input.supplieddata',),
        ),
    ]
