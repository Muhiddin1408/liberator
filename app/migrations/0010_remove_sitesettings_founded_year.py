from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_translated_slugs'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sitesettings',
            name='founded_year',
        ),
    ]
