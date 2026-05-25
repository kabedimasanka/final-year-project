# Generated for the custom admin dashboard metrics.

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("members", "0002_location_reservation_price_reservation_status_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="reservation",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="reservation",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
