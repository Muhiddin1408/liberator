"""
Replaces the old User-linked Staff model with a standalone profile model
designed for the public team page (full_name, position, slug, social links,
RichText specialization/practice, ordering, soft-deactivation, timestamps).

The old Staff table is dropped and a new one is created. Any rows previously
stored in the User-linked Staff table will be lost — re-enter them through
the admin after running ``python manage.py migrate``.
"""
from django.db import migrations, models
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0004_alter_service_description_en_and_more"),
    ]

    operations = [
        migrations.DeleteModel(name="Staff"),
        migrations.CreateModel(
            name="Staff",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("full_name", models.CharField(max_length=200, verbose_name="F.I.O")),
                ("position", models.CharField(max_length=200, verbose_name="Lavozim")),
                ("short_description", models.CharField(
                    blank=True, max_length=300,
                    help_text="Card ostida ko'rinadigan 1-2 qatorlik qisqa matn.",
                    verbose_name="Qisqa tavsif",
                )),
                ("specialization", ckeditor.fields.RichTextField(blank=True, verbose_name="Mutaxassislik")),
                ("practice", ckeditor.fields.RichTextField(blank=True, verbose_name="Amaliyot")),
                ("image", models.ImageField(
                    blank=True, null=True, upload_to="staff/%Y/%m/",
                    help_text="Tavsiya: 600x700px, kvadratga yaqin format.",
                    verbose_name="Rasm",
                )),
                ("phone", models.CharField(blank=True, max_length=32, verbose_name="Telefon")),
                ("email", models.EmailField(blank=True, max_length=254, verbose_name="Email")),
                ("telegram", models.URLField(blank=True, verbose_name="Telegram")),
                ("linkedin", models.URLField(blank=True, verbose_name="LinkedIn")),
                ("slug", models.SlugField(blank=True, max_length=220, unique=True, verbose_name="Slug")),
                ("order", models.PositiveIntegerField(db_index=True, default=0, verbose_name="Tartib")),
                ("is_active", models.BooleanField(db_index=True, default=True, verbose_name="Faol")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Yangilangan")),
            ],
            options={
                "verbose_name": "Jamoa a'zosi",
                "verbose_name_plural": "Jamoa",
                "ordering": ("order", "id"),
            },
        ),
        migrations.AddIndex(
            model_name="staff",
            index=models.Index(fields=["is_active", "order"], name="app_staff_is_acti_idx"),
        ),
    ]
