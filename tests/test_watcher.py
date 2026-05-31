import sqlite3
import tempfile
import unittest
from pathlib import Path

from zotman.watcher import PDFRenameHandler, extract_year_from_db, get_storage_key_from_path


class WatcherTests(unittest.TestCase):
    def test_get_storage_key_from_path(self):
        path = "/Users/example/Zotero/storage/ABC123/Author - Title.pdf"

        self.assertEqual(get_storage_key_from_path(path), "ABC123")

    def test_extract_year_from_db_reads_parent_item_date(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "zotero.sqlite"
            with sqlite3.connect(db_path) as con:
                con.execute(
                    """
                    CREATE TABLE itemAttachments (
                        parentItemID INTEGER,
                        linkMode INTEGER,
                        path TEXT
                    )
                    """
                )
                con.execute("CREATE TABLE fields (fieldID INTEGER, fieldName TEXT)")
                con.execute(
                    "CREATE TABLE itemData (itemID INTEGER, fieldID INTEGER, valueID INTEGER)"
                )
                con.execute(
                    "CREATE TABLE itemDataValues (valueID INTEGER, value TEXT)"
                )
                con.execute(
                    "INSERT INTO itemAttachments VALUES (?, ?, ?)",
                    (42, 0, "storage/ABC123/paper.pdf"),
                )
                con.execute("INSERT INTO fields VALUES (?, ?)", (1, "date"))
                con.execute("INSERT INTO itemData VALUES (?, ?, ?)", (42, 1, 7))
                con.execute("INSERT INTO itemDataValues VALUES (?, ?)", (7, "2024"))

            self.assertEqual(extract_year_from_db(db_path, "ABC123"), "2024")

    def test_target_dir_includes_year_when_available(self):
        handler = PDFRenameHandler("/tmp/cloud", "/tmp/zotero.sqlite")

        self.assertEqual(
            handler.get_target_dir("AI", "2024"),
            Path("/tmp/cloud/AI/2024"),
        )
        self.assertEqual(handler.get_target_dir("AI", None), Path("/tmp/cloud/AI"))


if __name__ == "__main__":
    unittest.main()
