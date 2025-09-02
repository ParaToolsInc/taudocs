#!/usr/bin/env python3
from collections import deque
from pathlib import Path
from typing import Dict, Set, Tuple
from lxml import etree

from config import ORIGINAL_SRC_DIR, MASTER_FILES, XI_NS

def _resolve_include(parent_xml: Path, href: str) -> Path:
    return (parent_xml.parent / href).resolve()

def _iter_includes_recursive(xml_path: Path) -> Tuple[Path, ...]:
    try:
        root = etree.fromstring(xml_path.read_bytes(), parser=etree.XMLParser(recover=True, no_network=True))
    except etree.XMLSyntaxError:
        return tuple()
    includes = []
    for el in root.iterfind(".//xi:include", namespaces={"xi": XI_NS}):
        href = el.get("href")
        if href:
            inc = _resolve_include(xml_path, href)
            if inc.exists():
                includes.append(inc)
    return tuple(includes)

def build_depth_map() -> Dict[Path, int]:
    """
    Compute minimal include depth for every XML reachable from the masters.
    depth 0 = master itself
    depth 1 = directly included by a master
    depth 2 = included by a wrapper (and so on)
    """
    depth: Dict[Path, int] = {}
    q: deque[Tuple[Path, int]] = deque()

    # Seed queue with masters at depth 0
    for name in MASTER_FILES:
        try:
            master_path = next(ORIGINAL_SRC_DIR.rglob(f"**/{name}"))
        except StopIteration:
            continue
        depth[master_path] = 0
        q.append((master_path, 0))

    visited: Set[Path] = set()
    while q:
        current, d = q.popleft()
        if current in visited:
            continue
        visited.add(current)

        for inc in _iter_includes_recursive(current):
            new_d = d + 1
            if inc not in depth or new_d < depth[inc]:
                depth[inc] = new_d
                q.append((inc, new_d))

    return depth