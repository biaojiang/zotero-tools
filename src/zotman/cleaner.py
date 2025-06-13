import os
import shutil
import sqlite3
from pathlib import Path


def expand(path):
    return os.path.expanduser(path)


def get_used_storage_dirs(sqlite_path):
    con = sqlite3.connect(sqlite_path)
    cur = con.cursor()
    cur.execute("""
        SELECT path FROM itemAttachments
        WHERE linkMode = 0 AND path IS NOT NULL
    """)
    used = set()
    for (path,) in cur.fetchall():
        parts = Path(path).parts
        if len(parts) >= 2 and parts[0] == "storage":
            used.add(parts[1])
    con.close()
    return used


def find_orphaned_dirs(storage_dir, used_dirs):
    orphaned = []
    for subdir in Path(storage_dir).iterdir():
        if subdir.is_dir() and subdir.name not in used_dirs:
            orphaned.append(subdir)
    return orphaned


def run_cleaner(storage_path, db_path):
    storage_path = expand(storage_path)
    db_path = expand(db_path)
    print("🔍 Scanning Zotero storage for orphaned folders...")
    used = get_used_storage_dirs(db_path)
    orphans = find_orphaned_dirs(storage_path, used)
    if not orphans:
        print("✅ No orphaned folders found.")
    else:
        print(f"⚠️ Found {len(orphans)} orphaned folders that may be safe to delete:\n")
        for folder in orphans:
            print(f"🗂️  {folder}")
        confirm = input("\nDelete these folders? (y/N): ").lower()
        if confirm == 'y':
            for folder in orphans:
                try:
                    shutil.rmtree(folder)
                    print(f"🗑️ Deleted: {folder}")
                except Exception as e:
                    print(f"❌ Failed to delete {folder}: {e}")
        else:
            print("❎ No changes made.")
