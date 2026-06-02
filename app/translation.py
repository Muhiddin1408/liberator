from modeltranslation.translator import register, TranslationOptions

from app.models import Staff


@register(Staff)
class StaffTranslationOptions(TranslationOptions):
    """Staff modeli uchun tarjima qilinadigan maydonlar.

    Har bir maydon uchun modeltranslation avtomatik ravishda
    `<maydon>_uz`, `<maydon>_ru`, `<maydon>_en` ustunlarini yaratadi.
    """

    fields = (
        "full_name",
        "position",
        "short_description",
        "specialization",
        "practice",
    )
