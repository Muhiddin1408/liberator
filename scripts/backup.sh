#!/usr/bin/env bash
# Kunlik zaxira: SQLite baza (onlayn, xavfsiz usulda) + media fayllar.
# Cron (har kuni 03:00):
#   0 3 * * * /srv/liberator/scripts/backup.sh >> /var/log/liberator-backup.log 2>&1
# Haftada bir marta backups/ papkasini boshqa server yoki bulutga nusxalang (rclone, rsync).
# Tiklashni sinab ko'ring: sqlite3 backups/db-YYYY-MM-DD.sqlite3 "PRAGMA integrity_check;"
set -euo pipefail

APP_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DB="${SQLITE_PATH:-$APP_DIR/db.sqlite3}"
DEST="${BACKUP_DIR:-$APP_DIR/backups}"
KEEP_DAYS="${KEEP_DAYS:-30}"
STAMP="$(date +%F)"

mkdir -p "$DEST"

# sqlite3 CLI bo'lmasa ham ishlaydi — Python'ning backup API'si orqali.
python3 - "$DB" "$DEST/db-$STAMP.sqlite3" <<'PY'
import sqlite3, sys
src, dst = sys.argv[1], sys.argv[2]
with sqlite3.connect(src) as source, sqlite3.connect(dst) as target:
    source.backup(target)
    assert target.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
PY
gzip -f "$DEST/db-$STAMP.sqlite3"

if [ -d "$APP_DIR/media" ]; then
    tar czf "$DEST/media-$STAMP.tar.gz" -C "$APP_DIR" media
fi

find "$DEST" -type f -mtime +"$KEEP_DAYS" -delete
echo "$(date '+%F %T') zaxira tayyor: $DEST"
