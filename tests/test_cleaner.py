import sqlite3
import tempfile
import unittest
from pathlib import Path

from zotman.cleaner import find_orphaned_dirs, get_used_storage_dirs


class CleanerTests(unittest.TestCase):
    def test_get_used_storage_dirs_reads_zotero_attachment_paths(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "zotero.sqlite"
            with sqlite3.connect(db_path) as con:
                con.execute(
                    "CREATE TABLE itemAttachments (linkMode INTEGER, path TEXT)"
                )
                con.executemany(
                    "INSERT INTO itemAttachments VALUES (?, ?)",
                    [
                        (0, "storage/ABC123/paper.pdf"),
                        (0, "storage/XYZ789/notes.pdf"),
                        (1, "storage/LINKED/file.pdf"),
                        (0, None),
                    ],
                )

            self.assertEqual(get_used_storage_dirs(db_path), {"ABC123", "XYZ789"})

    def test_find_orphaned_dirs_ignores_used_storage_dirs(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            storage_dir = Path(tmpdir)
            used_dir = storage_dir / "ABC123"
            orphan_dir = storage_dir / "ORPHAN"
            used_dir.mkdir()
            orphan_dir.mkdir()
            (storage_dir / "file.txt").write_text("not a dir")

            self.assertEqual(find_orphaned_dirs(storage_dir, {"ABC123"}), [orphan_dir])


if __name__ == "__main__":
    unittest.main()
