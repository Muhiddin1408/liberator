from whitenoise.storage import CompressedManifestStaticFilesStorage


class LenientManifestStaticFilesStorage(CompressedManifestStaticFilesStorage):
    """Manifestda bo'lmagan nom uchun xato o'rniga oddiy URL qaytaradi.

    Jazzmin shabloni `{% static 'vendor/bootswatch' %}` deb papkaga murojaat qiladi;
    qattiq (strict) manifest rejimida bu ValueError beradi va admin 500 bo'ladi.
    """

    manifest_strict = False
