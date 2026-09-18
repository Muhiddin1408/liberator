"""Yangi murojaat haqida firmaga xabar berish: email va Telegram."""
import json
import logging
import urllib.request
from html import escape

from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


def _lead_lines(lead):
    lines = [
        ("Turi", lead.get_kind_display()),
        ("Ism", lead.full_name),
        ("Telefon", lead.phone),
        ("Email", lead.email),
        ("Yo'nalish", lead.service.name if lead.service else ""),
        ("Advokat", lead.staff.full_name if lead.staff else ""),
        ("Til", lead.language),
        ("Sahifa", lead.source_page),
    ]
    return [(label, value) for label, value in lines if value]


def notify_email(lead):
    recipients = settings.LEAD_NOTIFY_EMAILS
    if not recipients:
        return
    body = "\n".join(f"{label}: {value}" for label, value in _lead_lines(lead))
    if lead.message:
        body += f"\n\nXabar:\n{lead.message}"
    try:
        send_mail(
            subject=f"Saytdan yangi murojaat: {lead.full_name}",
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipients,
        )
    except Exception:  # noqa: BLE001 — xabarnoma xatosi murojaatni yo'qotmasin
        logger.exception("Murojaat #%s uchun email yuborilmadi", lead.pk)


def notify_telegram(lead):
    token, chat_id = settings.TELEGRAM_BOT_TOKEN, settings.TELEGRAM_CHAT_ID
    if not (token and chat_id):
        return
    text = "🔔 <b>Saytdan yangi murojaat</b>\n\n" + "\n".join(
        f"<b>{escape(label)}:</b> {escape(str(value))}" for label, value in _lead_lines(lead)
    )
    if lead.message:
        text += f"\n\n{escape(lead.message[:3000])}"
    payload = json.dumps({"chat_id": chat_id, "text": text, "parse_mode": "HTML"}).encode()
    request = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    try:
        urllib.request.urlopen(request, timeout=5).close()
    except Exception:  # noqa: BLE001
        logger.exception("Murojaat #%s uchun Telegram xabari yuborilmadi", lead.pk)


def notify_new_lead(lead):
    notify_telegram(lead)
    notify_email(lead)
