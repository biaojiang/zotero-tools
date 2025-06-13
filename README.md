# Zotman

[![PyPI version](https://img.shields.io/pypi/v/zotman)](https://pypi.org/project/zotman/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PyPI Downloads](https://static.pepy.tech/badge/zotman)](https://pepy.tech/projects/zotman)

**Zotman** is a CLI toolset for managing Zotero PDF attachments using linked files in a structured Cloud (default: Dropbox) folder.

It supports:
- Automatically moving renamed PDFs from Zotero’s storage into a structured subject/year Cloud folder
- Extracting the **published year** from Zotero’s database to organize PDFs
- Cleaning up **orphaned Zotero storage folders** not linked to any library item

---

## 📦 Installation

```bash
pip install zotman
```

---

## 🚀 Usage

### Move renamed Zotero PDFs

```
zotman move --cloud ~/Dropbox/Zotero
```

This will:

- Watch `~/Zotero/storage` for PDFs renamed by Zotero
- Prompt you for a subject (e.g., `AI`, `ML`)
- Look up the **published year** from `zotero.sqlite`
- Move the file to:
	```
	~/Dropbox/Zotero/<Subject>/<Year>/Author et al. - Title.pdf
	```

The `--cloud` option allows you to set any base folder (e.g., Dropbox, Google Drive, OneDrive). The default is `~/Dropbox/Zotero`.

Then, manually re-link the file in Zotero:

> Right-click item → Attach Link to File…

---

### Clean orphaned storage folders

```bash
zotman clean
```

This will:
- Read `zotero.sqlite`
- Identify unused subfolders in `~/Zotero/storage`
- Prompt before deletion

---

## 🧠 Why use Zotman?

Zotero stores files in random folders without year structure. Zotman helps:
- Organize files by **subject and year**
- Keep filenames clean
- Maintain a consistent Cloud (e.g., Dropbox)-based linked file setup
- Remove clutter from old unlinked folders

---

## 🛠 Future Plans

- Automatic re-linking
- Year range filters
- GUI and batch operations

---

## 📄 License

MIT License
