#!/usr/bin/env python3
from pathlib import Path

# Base paths
CWD = Path.cwd()
ORIGINAL_SRC_DIR = CWD / "original_docbook"
DEST_BASE_DIR = CWD / "src"
PAGES_DIR = DEST_BASE_DIR / "modules" / "ROOT" / "pages"
IMAGES_DIR = DEST_BASE_DIR / "modules" / "ROOT" / "assets" / "images"

# Top-level DocBook masters (become top-level AsciiDoc books)
MASTER_FILES = [
    "usersguide.xml",
    "installguide.xml",
    "referenceguide.xml",
]

# Assets
LOGO_FILENAME = "NewTauLogo.png"

# Namespaces
XI_NS = "http://www.w3.org/2001/XInclude"