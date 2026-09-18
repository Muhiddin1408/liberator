import time

from django import forms
from django.core import signing
from django.utils.translation import gettext_lazy as _

from app.models import ConsultationRequest, ServiceCategory, Staff

# Botlar formani sahifa ochilgan zahoti yuboradi — odam kamida bir necha soniya sarflaydi.
MIN_FILL_SECONDS = 3
FORM_TOKEN_MAX_AGE = 60 * 60 * 6
_signer = signing.TimestampSigner(salt="consultation-form")


def make_form_token():
    return _signer.sign(str(int(time.time())))


class ConsultationForm(forms.ModelForm):
    """Konsultatsiya va qayta qo'ng'iroq uchun yagona forma.

    Spam himoyasi: honeypot maydon (`website`), imzolangan vaqt belgisi
    (`form_token`) va view'dagi IP bo'yicha cheklov.
    """

    website = forms.CharField(required=False, widget=forms.TextInput(attrs={
        "tabindex": "-1", "autocomplete": "off",
    }))
    form_token = forms.CharField(widget=forms.HiddenInput)
    consent = forms.BooleanField(
        required=True,
        label=_("Shaxsiy ma’lumotlarimni qayta ishlashga roziman"),
        error_messages={"required": _("Davom etish uchun roziligingiz kerak.")},
    )

    class Meta:
        model = ConsultationRequest
        fields = ("kind", "full_name", "phone", "email", "service", "staff", "message", "source_page")
        widgets = {
            "kind": forms.HiddenInput,
            "staff": forms.HiddenInput,
            "source_page": forms.HiddenInput,
            "full_name": forms.TextInput(attrs={"autocomplete": "name"}),
            "phone": forms.TextInput(attrs={
                "type": "tel", "autocomplete": "tel", "inputmode": "tel", "placeholder": "+998 __ ___ __ __",
            }),
            "email": forms.EmailInput(attrs={"autocomplete": "email"}),
            "message": forms.Textarea(attrs={"rows": 4}),
        }
        labels = {
            "full_name": _("Ismingiz"),
            "phone": _("Telefon raqamingiz"),
            "email": _("Email (ixtiyoriy)"),
            "service": _("Yo‘nalish"),
            "message": _("Masalangizni qisqacha yozing"),
        }
        error_messages = {
            "phone": {"invalid": _("Telefon raqamini to‘g‘ri kiriting, masalan: +998 90 123 45 67")},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "service" in self.fields:
            self.fields["service"].queryset = ServiceCategory.objects.active()
            self.fields["service"].empty_label = _("— Tanlang —")
            self.fields["service"].label_from_instance = lambda obj: obj.tr("name")
        if "staff" in self.fields:
            self.fields["staff"].queryset = Staff.objects.filter(is_active=True)
        self.fields["kind"].required = False
        if not self.is_bound:
            self.initial.setdefault("form_token", make_form_token())
            self.initial.setdefault("kind", ConsultationRequest.KIND_CONSULTATION)

    def clean_kind(self):
        return self.cleaned_data.get("kind") or ConsultationRequest.KIND_CONSULTATION

    def clean_full_name(self):
        return " ".join(self.cleaned_data["full_name"].split())

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("website"):
            raise forms.ValidationError(_("So‘rov rad etildi."), code="spam")
        try:
            issued = int(_signer.unsign(self.data.get("form_token", ""), max_age=FORM_TOKEN_MAX_AGE))
        except (signing.BadSignature, ValueError):
            raise forms.ValidationError(_("Sahifa eskirgan. Iltimos, sahifani yangilab qayta yuboring."),
                                        code="token")
        if time.time() - issued < MIN_FILL_SECONDS:
            raise forms.ValidationError(_("So‘rov rad etildi."), code="spam")
        kind = cleaned.get("kind")
        if kind == ConsultationRequest.KIND_CONSULTATION and not cleaned.get("message"):
            self.add_error("message", _("Masalangizni qisqacha yozing."))
        return cleaned


class CallbackForm(ConsultationForm):
    """Faqat ism va telefon — 10 soniyada to'ldiriladi."""

    class Meta(ConsultationForm.Meta):
        fields = ("kind", "full_name", "phone", "source_page")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.is_bound:
            self.initial["kind"] = ConsultationRequest.KIND_CALLBACK
