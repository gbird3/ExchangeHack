from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('smh2', '0002_stock'),
    ]

    operations = [
        migrations.CreateModel(
            name='tenK',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('lang', models.CharField(max_length=10)),
                ('location', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('screen_name', models.CharField(max_length=100)),
                ('text', models.CharField(max_length=1000)),
                ('text_polarity', models.DecimalField(decimal_places=10, max_digits=10)),
                ('text_subjectivity', models.DecimalField(decimal_places=10, max_digits=10)),
                ('time_zone', models.CharField(max_length=100)),
                ('verified', models.CharField(max_length=100)),
            ],
        ),
    ]
