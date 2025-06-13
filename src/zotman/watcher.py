import os
import shutil
import sqlite3
import time
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


def expand(path):
    return os.path.expanduser(path)


def get_storage_key_from_path(path):
    parts = Path(path).parts
    try:
        index = parts.index("storage")
        return parts[index + 1]
    except (ValueError, IndexError):
        return None


def extract_year_from_db(db_path, storage_key):
    db_path = expand(db_path)
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute(
        """
        SELECT itemAttachments.parentItemID
        FROM itemAttachments
        WHERE itemAttachments.linkMode = 0 AND itemAttachments.path LIKE ?
    """,
        (f"storage/{storage_key}/%",),
    )
    row = cur.fetchone()
    if not row:
        con.close()
        return None
    parent_id = row[0]

    cur.execute(
        """
        SELECT itemDataValues.value
        FROM itemData
        JOIN fields ON itemData.fieldID = fields.fieldID
        JOIN itemDataValues ON itemData.valueID = itemDataValues.valueID
        WHERE itemData.itemID = ? AND fields.fieldName = 'date'
    """,
        (parent_id,),
    )
    row = cur.fetchone()
    con.close()
    if not row:
        return None

    date_str = row[0]
    for part in date_str.split():
        if part[:4].isdigit():
            return part[:4]
    return None


class PDFRenameHandler(FileSystemEventHandler):
    def __init__(self, cloud_base, zotero_db):
        self.cloud_base = Path(expand(cloud_base))
        self.zotero_db = zotero_db

    def on_moved(self, event):
        if not event.is_directory and event.dest_path.lower().endswith(".pdf"):
            filename = os.path.basename(event.dest_path)
            print(f"\n📄 PDF renamed: {filename}")
            subject = input("Enter subject folder (e.g., AI, ML, Robotics): ").strip()
            storage_key = get_storage_key_from_path(event.dest_path)
            year = extract_year_from_db(self.zotero_db, storage_key)
            target_dir = self.cloud_base / subject
            target_dir.mkdir(parents=True, exist_ok=True)

            name, ext = os.path.splitext(filename)
            parts = name.split(" - ", 1)  # Expect 'Author et al.' and 'Title'

            if year and len(parts) == 2 and year not in name:
                new_filename = f"{year} - {name}{ext}"
            else:
                new_filename = filename
            dst_path = target_dir / new_filename
            try:
                shutil.move(event.dest_path, dst_path)
                print(f"✅ Moved to: {dst_path}")
                print(
                    "➡️  In Zotero: Right-click parent item > Add Attachment > Attach Link to File..."
                )
            except Exception as e:
                print(f"❌ Failed to move file: {e}")


def run_watcher(storage_path, cloud_path):
    storage_path = expand(storage_path)
    cloud_path = expand(cloud_path)
    zotero_db = expand("~/Zotero/zotero.sqlite")
    event_handler = PDFRenameHandler(cloud_path, zotero_db)
    observer = Observer()
    observer.schedule(event_handler, path=storage_path, recursive=True)
    print(f"👀 Watching {storage_path} for renamed PDFs...")
    print("Press Ctrl+C to stop.\n")
    try:
        observer.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n🛑 Stopped watching.")
    observer.join()
