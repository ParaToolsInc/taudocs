#!/usr/bin/env python3
import shutil
import sys
from pathlib import Path

from config import ORIGINAL_SRC_DIR, MASTER_FILES
from include_graph import build_depth_map
from converter import init_directories, process_xml_file

def main():
    # Require Pandoc; GraphicsMagick optional (only needed for GIF -> PNG)
    if not shutil.which("pandoc"):
        print("FATAL: 'pandoc' not in PATH.", file=sys.stderr)
        sys.exit(1)
    if not shutil.which("gm"):
        print("NOTE: 'gm' (GraphicsMagick) not found; GIFs, if any, will not be converted to PNG.")

    init_directories()

    print("=== Analyzing include graph ===")
    depth_map = build_depth_map()

    # Ensure masters exist and are depth 0
    masters: list[Path] = []
    for name in MASTER_FILES:
        try:
            m = next(ORIGINAL_SRC_DIR.rglob(f"**/{name}"))
        except StopIteration:
            print(f"FATAL: Master file not found in '{ORIGINAL_SRC_DIR}': {name}", file=sys.stderr)
            sys.exit(1)
        depth_map[m] = 0
        masters.append(m)

    print("=== Converting documents ===")
    # Process masters first
    for m in sorted(masters):
        process_xml_file(m, depth_map)

    # Then process all other reachable files so includes resolve on disk
    others = sorted([p for p in depth_map.keys() if p not in masters])
    for p in others:
        process_xml_file(p, depth_map)

    print(f"\n=== Migration Complete. Processed files: {len(masters) + len(others)} ===")

if __name__ == "__main__":
    main()