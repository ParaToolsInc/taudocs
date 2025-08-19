#!/usr/bin/env python3

import os
import re
import sys
import shutil
import subprocess
from pathlib import Path
from lxml import etree

# --- Configuration ---
CWD = Path.cwd()
ORIGINAL_SRC_DIR = CWD / "original_docbook"
DEST_BASE_DIR = CWD / "src"
PAGES_DIR = DEST_BASE_DIR / "modules/ROOT/pages"
IMAGES_DIR = DEST_BASE_DIR / "modules/ROOT/assets/images"
LOGO_FILENAME = "NewTauLogo.png"

MASTER_FILES = [
    "usersguide/usersguide.xml",
    "installguide/installguide.xml",
    "referenceguide/referenceguide.xml",
]

PROCESSED_FILES = set()
COPIED_IMAGES = set()
XI_NS = "http://www.w3.org/2001/XInclude"

# This map is the single source of truth for heading levels.
HEADING_LEVEL_MAP = {
    "book": 1, "part": 2, "chapter": 2, "preface": 2, "appendix": 2,
    "section": 3, "sect1": 3, "sect2": 4, "sect3": 5, "sect4": 5, "sect5": 5,
}

# --- Helper Functions ---
def init_directories():
    print("=== Cleaning stale output directories ===")
    if PAGES_DIR.exists(): shutil.rmtree(PAGES_DIR)
    if IMAGES_DIR.exists(): shutil.rmtree(IMAGES_DIR)
    PAGES_DIR.mkdir(parents=True, exist_ok=True)
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    logo_source = ORIGINAL_SRC_DIR / "usersguide" / LOGO_FILENAME
    if logo_source.exists():
        print(f"  -> Copying project logo: {LOGO_FILENAME}")
        shutil.copy(logo_source, IMAGES_DIR / LOGO_FILENAME)
    else:
        print(f"  -> WARNING: Project logo not found at {logo_source}")    

def sanitize_id(id_string: str) -> str:
    if not id_string: return ""
    return id_string.replace('.', '-')

def sanitize_tree_ids(element):
    if not isinstance(element.tag, str): return
    # ... (sanitization logic remains the same) ...

# --- Conversion Functions ---

def convert_refsynopsisdiv(element) -> str:
    """Converts a DocBook <refsynopsisdiv> into a formatted AsciiDoc listing block."""
    synopsis = element.find('.//cmdsynopsis')
    if synopsis is None:
        return ""

    parts = []
    for item in synopsis:
        if not isinstance(item.tag, str):
            continue

        tag = etree.QName(item).localname
        text = ''.join(item.itertext()).strip()

        if tag == 'command':
            parts.append(f"*{text}*") # Make the command bold
        elif tag == 'arg':
            arg_text = text
            # Check for <replaceable> which indicates a variable
            replaceable = item.find('.//replaceable')
            if replaceable is not None and replaceable.text:
                arg_text = f"<{replaceable.text.strip()}>"

            # Check if optional
            if item.get('choice') == 'opt':
                # For complex optional args, just wrap the whole thing
                if len(item) > 1:
                     parts.append(f"[{''.join(item.itertext()).strip()}]")
                else:
                     parts.append(f"[{arg_text}]")
            else:
                parts.append(arg_text)

    # Join all parts with spaces and wrap in a source block
    full_command = " ".join(parts)
    return f"[source, subs=\"+quotes\"]\n----\n{full_command}\n----"

def convert_para(element, abs_xml_path, level):
    # This list will hold all the pieces of the paragraph in order.
    content_parts = []
    
    # Start with the initial text of the <para> tag itself.
    if element.text:
        content_parts.append(element.text)

    # Loop through all child elements (like <literal>, <xref>, etc.)
    for child in element:
        # Recursively convert the child element to its AsciiDoc form.
        # Pass the level, though it's often unused by inline elements.
        child_adoc = convert_element_to_adoc(child, abs_xml_path, level=level)
        content_parts.append(child_adoc)
        
        # IMPORTANT: Also append the text that comes *after* the child tag.
        if child.tail:
            content_parts.append(child.tail)

    # Join all the pieces with spaces, and then normalize all whitespace
    # to prevent extra spaces or weird line breaks within the paragraph.
    full_para = "".join(content_parts)
    return ' '.join(full_para.split())

def convert_element_to_adoc(element, abs_xml_path, level: int):
    if not isinstance(element.tag, str): return ""
    tag_name = etree.QName(element).localname
    output = []

    # --- DYNAMIC HEADING LOGIC ---
    if tag_name in HEADING_LEVEL_MAP:
        title_element = element.find('title')
        title = title_element.text.strip() if title_element is not None and title_element.text else ""
        if title:
            if elem_id := element.get('id') or element.get('{http://www.w3.org/XML/1998/namespace}id'):
                output.append(f"[[{sanitize_id(elem_id)}]]")
            output.append(f"{'=' * level} {title}")
        # Process children at the next level, ensuring they are separated by newlines
        child_content = [convert_element_to_adoc(child, abs_xml_path, level=level + 1) for child in element if isinstance(child.tag, str) and etree.QName(child).localname != 'title']
        output.append("\n\n".join(filter(None, child_content)))

    elif tag_name == 'para':
        output.append(convert_para(element, abs_xml_path, level))
        
    elif element.tag == f"{{{XI_NS}}}include":
        href = element.get("href")
        include_path = (abs_xml_path.parent / href).resolve()
        process_file(include_path)
        rel_include_path = include_path.relative_to(ORIGINAL_SRC_DIR)
        adoc_target_path = (PAGES_DIR / rel_include_path).with_suffix(".adoc")
        relative_include = os.path.relpath(adoc_target_path, (PAGES_DIR / abs_xml_path.relative_to(ORIGINAL_SRC_DIR)).parent)
        output.append(f":leveloffset: +1\ninclude::{relative_include}[]\n:leveloffset: -1")
    elif tag_name == 'refsynopsisdiv':
        output.append(convert_refsynopsisdiv(element))
    elif tag_name == 'figure':
        output.append(convert_figure(element, abs_xml_path))
    elif tag_name == 'itemizedlist':
        output.append(convert_list(element, abs_xml_path))
    elif tag_name == 'xref':
        return f"<<{sanitize_id(element.get('linkend'))}>>" # Return directly for inline
    elif tag_name == 'link':
        return f"<<{sanitize_id(element.get('linkend'))},{element.text or ''}>>" # Return directly
    elif tag_name == 'ulink':
        return f"{element.get('url')}[{element.text or ''}]" # Return directly
    elif tag_name == 'literal':
        return f"`{element.text}`" # Return directly
    elif tag_name == 'screen' or tag_name == 'programlisting':
        text = ''.join(element.itertext()).strip()
        output.append(f"[source]\n----\n{text}\n----")
    elif tag_name in ['title', 'bookinfo', 'simplesect', 'refmeta', 'manvolnum', 'refentrytitle', 'refname', 'refpurpose', 'part', 'refentry', 'refnamediv']:
        # These are structural or handled by parents, ignore them.
        pass
    else:
        output.append(convert_xml_snippet(element, abs_xml_path.parent))

    return "\n".join(output)


def convert_list(element, abs_xml_path):
    """Converts an <itemizedlist> to an AsciiDoc list."""
    output = []
    for item in element.findall('.//listitem'):
        # Get all text inside the para, including tail text of child elements
        text = ''.join(item.find('.//para').itertext()).strip()
        output.append(f"* {text}")
    return "\n".join(output) + "\n"

def convert_figure(element, abs_xml_path: Path) -> str:
    output = []
    if fig_id := element.get('id') or element.get('{http://www.w3.org/XML/1998/namespace}id'):
        output.append(f"[[{fig_id}]]")
    title_element = element.find('title')
    title = title_element.text if title_element is not None else ''
    if title: output.append(f".{title}")
    imagedata = element.find('.//imagedata')
    if imagedata is None: return ''
    if not (fileref := imagedata.get('fileref')): return ''
    source_image_path = (abs_xml_path.parent / fileref).resolve()
    image_basename = source_image_path.name
    is_gif = source_image_path.suffix.lower() == '.gif'
    if is_gif:
        image_basename = source_image_path.with_suffix('.png').name
        dest_image_path = IMAGES_DIR / image_basename
    else:
        dest_image_path = IMAGES_DIR / image_basename
    if source_image_path.exists():
        if dest_image_path not in COPIED_IMAGES:
            if is_gif:
                print(f"  -> Converting {source_image_path.name} to PNG...")
                try:
                    subprocess.run(
                        ["gm", "convert", str(source_image_path), str(dest_image_path)],
                        check=True, capture_output=True, text=True
                    )
                    COPIED_IMAGES.add(dest_image_path)
                except (subprocess.CalledProcessError, FileNotFoundError) as e:
                    print(f"  -> WARNING: Failed to convert {source_image_path.name}. Check that 'gm' is installed. Error: {e.stderr}")
                    # Fallback to copying the original GIF
                    shutil.copy(source_image_path, IMAGES_DIR / source_image_path.name)
                    COPIED_IMAGES.add(IMAGES_DIR / source_image_path.name)
                    image_basename = source_image_path.name # Revert basename to .gif
            else:
                shutil.copy(source_image_path, dest_image_path)
                COPIED_IMAGES.add(dest_image_path)
    else:
        print(f"  -> WARNING: Image file not found: {source_image_path}")
        return ''
    alt_text = title if title else source_image_path.stem
    attributes = [alt_text]
    if width := imagedata.get('width'): attributes.append(f'width="{width}"')
    if align := imagedata.get('align'): attributes.append(f'align="{align}"')
    output.append(f"image::{image_basename}[{','.join(attributes)}]")
    return "\n".join(output)


def convert_xml_snippet(element, original_dir: Path) -> str:
    # ... (Pandoc fallback is unchanged) ...
    xml_snippet = etree.tostring(element, encoding='unicode')
    wrapped_snippet = f'<!DOCTYPE article PUBLIC "-//OASIS//DTD DocBook XML V4.5//EN" "http://www.oasis-open.org/docbook/xml/4.5/docbookx.dtd"><article xmlns:xi="http://www.w3.org/2001/XInclude">{xml_snippet}</article>'
    try:
        result = subprocess.run(
            ["pandoc", "--from", "docbook", "--to", "asciidoc", "--wrap=none",
             f"--resource-path={original_dir}", f"--extract-media={IMAGES_DIR}"],
            input=wrapped_snippet, text=True, capture_output=True, check=True)
        # Clean up pandoc's output
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"FATAL: Pandoc conversion failed for snippet:\n{xml_snippet}", file=sys.stderr); print(f"--- Pandoc Error ---\n{e.stderr}", file=sys.stderr); sys.exit(1)


def process_file(xml_path: Path):
    abs_xml_path = xml_path.resolve()
    if not abs_xml_path.exists():
        print(f"FATAL: Source file not found: {xml_path}", file=sys.stderr); sys.exit(1)

    if abs_xml_path in PROCESSED_FILES: return
    print(f"Processing: {abs_xml_path}")
    PROCESSED_FILES.add(abs_xml_path)

    relative_path = abs_xml_path.relative_to(ORIGINAL_SRC_DIR)
    output_path = (PAGES_DIR / relative_path).with_suffix(".adoc")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    parser = etree.XMLParser(recover=True, no_network=True)
    root = etree.fromstring(xml_path.read_bytes(), parser)
    sanitize_tree_ids(root)

    with open(output_path, "w", encoding='utf-8') as f:
        is_master = any(abs_xml_path.samefile(ORIGINAL_SRC_DIR / mf) for mf in MASTER_FILES)

        title_element = root.find('title')
        if title_element is None: title_element = root.find('.//refnamediv/refname')
        title = title_element.text.strip() if title_element is not None and title_element.text else "Untitled"

        if is_master:
            # Define doctype and title FIRST
            f.write(f":doctype: book\n:imagesdir: ../../assets/images\n\n")
            if root_id := root.get('id') or root.get('{http://www.w3.org/XML/1998/namespace}id'):
                f.write(f'[[{sanitize_id(root_id)}]]\n')
            f.write(f"= {title}\n\n") # The {doc-title} is now set

            f.write("include::../../partials/_header.adoc[]\n\n")
            f.write(":toc: macro\ntoc::[]\n\n")
        else:
            # The logic for non-master files is already correct
            if root_id := root.get('id') or root.get('{http://www.w3.org/XML/1998/namespace}id'):
                f.write(f'[[{sanitize_id(root_id)}]]\n')
            f.write(f"= {title}\n\n")

        # Start processing the children of the root at level 2 (==)
        for element in root:
            if not isinstance(element.tag, str): continue
            if etree.QName(element).localname in ['title', 'bookinfo', 'refmeta']:
                continue
            content = convert_element_to_adoc(element, abs_xml_path, level=2)
            if content:
                f.write(content)
                f.write("\n\n")

    print(f"  Completed: {abs_xml_path} -> {output_path}")


def main():
    if not all(shutil.which(cmd) for cmd in ["pandoc", "gm"]):
        print("FATAL: pandoc and/or gm are not installed or in your PATH.", file=sys.stderr); sys.exit(1)
    
    init_directories()
    
    for master_file in MASTER_FILES:
        print(f"\n=== Processing Master File: {master_file} ===")
        process_file(ORIGINAL_SRC_DIR / master_file)
        
    print("\n\n=== Migration Complete ===")
    print(f"Processed {len(PROCESSED_FILES)} files.")
    print("\nNext steps:")
    print("1. Please review the generated files and run `make`.")
    print("2. If successful, you can remove the script and the 'original_docbook' directory.")

if __name__ == "__main__":
    main()
