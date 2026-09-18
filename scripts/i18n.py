#!/usr/bin/env python
"""Tarjima fayllarini yangilash va kompilyatsiya qilish (GNU gettext o'rnatilmagan serverlar uchun).

    python scripts/i18n.py          # shablon va koddan matnlarni yig'ib, .po ni yangilaydi va .mo ni yig'adi
    python scripts/i18n.py compile  # faqat .po -> .mo

Asosiy til — o'zbekcha: msgid o'zbekcha matn, tarjimalar locale/ru va locale/en da.
locale/uz — admin panel (Django admin + Jazzmin) uchun yetishmayotgan o'zbekcha tarjimalar, qo'lda yuritiladi.
GNU gettext o'rnatilgan bo'lsa, odatiy `makemessages` / `compilemessages` ham ishlaydi.
"""
import ast
import os
import sys
from pathlib import Path

import polib

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")
os.environ.setdefault("DEBUG", "1")

LANGS = ("ru", "en")
PY_DIRS = ("app", "conf")
GETTEXT_NAMES = {"_", "gettext", "gettext_lazy", "pgettext", "pgettext_lazy"}


def extract_templates():
    import django
    from django.template import engines
    from django.templatetags.i18n import BlockTranslateNode, TranslateNode

    django.setup()
    engine = engines["django"].engine
    found = {}
    for path in sorted((BASE_DIR / "template").rglob("*.html")):
        template = engine.from_string(path.read_text(encoding="utf-8"))
        rel = path.relative_to(BASE_DIR)
        for node in template.nodelist.get_nodes_by_type(TranslateNode):
            var = node.filter_expression.var
            literal = getattr(var, "literal", None)
            if isinstance(literal, str):
                found.setdefault((None, literal.replace("%", "%%")), set()).add(str(rel))
        for node in template.nodelist.get_nodes_by_type(BlockTranslateNode):
            msgid, _ = node.render_token_list(node.singular)
            found.setdefault((None, msgid), set()).add(str(rel))
    return found


def extract_python():
    found = {}
    for folder in PY_DIRS:
        for path in sorted((BASE_DIR / folder).rglob("*.py")):
            if "migrations" in path.parts:
                continue
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                        and node.func.id in GETTEXT_NAMES and node.args):
                    continue
                # pgettext(context, message) — birinchi argument kontekst.
                if node.func.id.startswith("p"):
                    if len(node.args) < 2 or not all(isinstance(a, ast.Constant) for a in node.args[:2]):
                        continue
                    key = (node.args[0].value, node.args[1].value)
                elif isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
                    key = (None, node.args[0].value)
                else:
                    continue
                found.setdefault(key, set()).add(str(path.relative_to(BASE_DIR)))
    return found


def po_path(lang):
    return BASE_DIR / "locale" / lang / "LC_MESSAGES" / "django.po"


def update_catalogs():
    messages = extract_templates()
    for key, refs in extract_python().items():
        messages.setdefault(key, set()).update(refs)

    for lang in LANGS:
        path = po_path(lang)
        po = polib.pofile(str(path)) if path.exists() else polib.POFile()
        po.metadata = {
            "Project-Id-Version": "liberator",
            "Language": lang,
            "MIME-Version": "1.0",
            "Content-Type": "text/plain; charset=UTF-8",
            "Content-Transfer-Encoding": "8bit",
            "Plural-Forms": ("nplurals=3; plural=(n%10==1 && n%100!=11 ? 0 : n%10>=2 && n%10<=4 && "
                             "(n%100<10 || n%100>=20) ? 1 : 2);") if lang == "ru" else "nplurals=2; plural=(n != 1);",
        }
        existing = {(entry.msgctxt, entry.msgid): entry for entry in po}
        new = polib.POFile()
        new.metadata = po.metadata
        for key in sorted(messages, key=lambda k: (k[0] or "", k[1])):
            ctx, msgid = key
            entry = existing.get(key) or polib.POEntry(msgctxt=ctx, msgid=msgid, msgstr="")
            entry.occurrences = [(ref, "") for ref in sorted(messages[key])]
            if "%(" in msgid and "python-format" not in entry.flags:
                entry.flags.append("python-format")
            new.append(entry)
        obsolete = [m for m in existing if m not in messages]
        new.save(str(path))
        untranslated = [e.msgid for e in new if not e.msgstr]
        print(f"{lang}: {len(new)} ta matn, tarjimasiz: {len(untranslated)}, eskirgan (o'chirildi): {len(obsolete)}")


def compile_catalogs():
    # locale/ ichidagi barcha .po: sayt (ru, en) va admin panel (uz: django + djangojs).
    for path in sorted((BASE_DIR / "locale").glob("*/LC_MESSAGES/*.po")):
        polib.pofile(str(path)).save_as_mofile(str(path.with_suffix(".mo")))
        print(path.with_suffix(".mo").relative_to(BASE_DIR))


if __name__ == "__main__":
    if sys.argv[1:] != ["compile"]:
        update_catalogs()
    compile_catalogs()
