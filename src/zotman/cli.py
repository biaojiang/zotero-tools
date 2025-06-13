import argparse
from zotman import watcher, cleaner


def main():
    parser = argparse.ArgumentParser(
        prog="zotman", description="Zotero attachment management CLI"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    move_parser = subparsers.add_parser(
        "move", help="Watch Zotero storage and move renamed PDFs to Dropbox"
    )
    move_parser.add_argument(
        "--storage",
        type=str,
        default="~/Zotero/storage",
        help="Path to Zotero storage folder",
    )
    # move_parser.add_argument("--dropbox", type=str, default="~/Dropbox/Zotero", help="Base Dropbox folder")
    move_parser.add_argument(
        "--cloud",
        type=str,
        default="~/Dropbox/Zotero",
        help="Base cloud folder (e.g., Dropbox, Google Drive, etc.)",
    )

    clean_parser = subparsers.add_parser(
        "clean", help="Clean orphaned folders in Zotero storage"
    )
    clean_parser.add_argument(
        "--storage",
        type=str,
        default="~/Zotero/storage",
        help="Path to Zotero storage folder",
    )
    clean_parser.add_argument(
        "--db",
        type=str,
        default="~/Zotero/zotero.sqlite",
        help="Path to Zotero SQLite database",
    )

    args = parser.parse_args()

    if args.command == "move":
        watcher.run_watcher(args.storage, args.cloud)
    elif args.command == "clean":
        cleaner.run_cleaner(args.storage, args.db)
