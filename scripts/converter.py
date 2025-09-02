#!/usr/bin/env python3
import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Set, List
from lxml import etree

from config import (
    ORIGINAL_SRC_DIR, PAGES_DIR, IMAGES_DIR,
    LOGO_FILENAME, MASTER_FILES, XI_NS
)

PROCESSED_FILES: Set[Path] = set()
COPIED_IMAGES: Set[Path] = set()

# Block-level DocBook elements when encountered inside a paragraph
BLOCK_TAGS = {
    "note", "important", "warning", "tip", "caution",
    "itemizedlist", "orderedlist", "variablelist",
    "figure", "informalfigure", "table", "informaltable",
    "screen", "programlisting",
    "funcsynopsis", "cmdsynopsis",
    "refentry",
    "formalpara",
}

def init_directories():
    # Clean outputs
    if PAGES_DIR.exists():
        shutil.rmtree(PAGES_DIR)
    if IMAGES_DIR.exists():
        shutil.rmtree(IMAGES_DIR)
    PAGES_DIR.mkdir(parents=True, exist_ok=True)
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    # Copy logo used by header partial (if present)
    logo_source = ORIGINAL_SRC_DIR / "usersguide" / LOGO_FILENAME
    if logo_source.exists():
        shutil.copy(logo_source, IMAGES_DIR)

def sanitize_id(id_string: str) -> str:
    if not id_string:
        return ""
    s = str(id_string).lower()
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r"[^a-z0-9\-._]", "", s)
    return s.strip("-")

def convert_figure(element, abs_xml_path: Path) -> str:
    out: List[str] = []
    if fig_id := element.get("id"):
        out.append(f"[[{sanitize_id(fig_id)}]]")

    title = ""
    te = element.find("title")
    if te is not None and (t := (te.text or "").strip()):
        title = f".{t}"
        out.append(title)

    imagedata = element.find(".//imagedata")
    if imagedata is None:
        return ""
    fileref = imagedata.get("fileref")
    if not fileref:
        print(f" -> WARNING: <imagedata> without 'fileref' in {abs_xml_path.name}. Skipping.")
        return ""

    source = (abs_xml_path.parent / fileref).resolve()
    image_basename = source.with_suffix(".png").name if source.suffix.lower() == ".gif" else source.name
    dest = IMAGES_DIR / image_basename
    if source.exists():
        if dest not in COPIED_IMAGES:
            if source.suffix.lower() == ".gif" and shutil.which("gm"):
                try:
                    subprocess.run(["gm", "convert", str(source), str(dest)], check=True, capture_output=True, text=True)
                except (subprocess.CalledProcessError, FileNotFoundError) as e:
                    print(f" -> FATAL: Failed to convert {source.name}. Details: {getattr(e, 'stderr', e)}")
                    return ""
            else:
                shutil.copy(source, dest)
            COPIED_IMAGES.add(dest)
    else:
        print(f" -> WARNING: Image file not found: {source}")
        return ""

    alt_text = title.lstrip(".") if title else source.stem
    attrs = [alt_text]
    if (w := imagedata.get("width")):
        attrs.append(f'width="{w}"')
    if (al := imagedata.get("align")):
        attrs.append(f'align="{al}"')
    out.append(f"image::{image_basename}[{','.join(attrs)}]")
    return "\n".join(out)

def convert_xml_snippet(element) -> str:
    xml_snippet = etree.tostring(element, encoding="unicode")
    wrapped = (
        '<!DOCTYPE article PUBLIC "-//OASIS//DTD DocBook XML V4.5//EN" '
        '"http://www.oasis-open.org/docbook/xml/4.5/docbookx.dtd">'
        f"<article>{xml_snippet}</article>"
    )
    try:
        return subprocess.run(
            ["pandoc", "--from", "docbook", "--to", "asciidoc", "--wrap=none"],
            input=wrapped, text=True, capture_output=True, check=True
        ).stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"FATAL: Pandoc failed for snippet:\n{xml_snippet}")
        raise

def docbook_next_level(tag_name: str, parent_level: int) -> int:
    # Logical DocBook level relative to a page title baseline (=)
    if tag_name in {"chapter", "appendix", "preface", "reference"}:
        return 2
    if tag_name == "section":
        return (parent_level + 1) if parent_level >= 2 else 2
    if tag_name == "sect1":
        return (parent_level + 1) if parent_level >= 2 else 2
    if tag_name == "sect2":
        return (parent_level + 1) if parent_level >= 3 else 3
    if tag_name == "sect3":
        return (parent_level + 1) if parent_level >= 4 else 4
    if tag_name == "sect4":
        return (parent_level + 1) if parent_level >= 5 else 5
    if tag_name == "sect5":
        return (parent_level + 1) if parent_level >= 6 else 6
    if tag_name == "refentry":
        return 2
    return max(2, parent_level)

def to_depth(baseline_depth: int, doc_level: int) -> int:
    # baseline_depth: number of '=' for the page title
    # doc_level: 2 => first section under the page title, 3 => subsection, etc.
    return baseline_depth + (doc_level - 1)

def convert_inline_like(element, abs_xml_path: Path, baseline_depth: int, parent_level: int) -> str:
    """Convert inline-ish elements for use inside paragraphs."""
    tag_name = etree.QName(element).localname
    if tag_name in {"literal", "command", "function", "option", "parameter", "filename"}:
        text = "".join(element.itertext())
        return f"`{text.strip()}`"
    if tag_name == "emphasis":
        inner = "".join(element.itertext())
        return f"*{inner.strip()}*" if element.get("role") == "bold" else f"_{inner.strip()}_"
    if tag_name == "firstterm":
        inner = "".join(element.itertext())
        return f"_{inner.strip()}_"
    if tag_name in {"xref", "link"}:
        if linkend := element.get("linkend"):
            return f"<<{sanitize_id(linkend)}>>"
        return ""
    if tag_name == "ulink":
        url = element.get("url")
        text = "".join(element.itertext()).strip()
        return f"link:{url}[{text or url}]"
    # Fallback to full conversion (safe)
    return convert_element(element, abs_xml_path, baseline_depth, parent_level)

def convert_para(element, abs_xml_path: Path, baseline_depth: int, parent_level: int) -> str:
    """Render a DocBook para, preserving block children as separate blocks."""
    pieces: List[str] = []
    inline_buf: List[str] = []

    def flush_inline():
        nonlocal inline_buf
        text = " ".join(" ".join(inline_buf).split()).strip()
        if text:
            pieces.append(text)
        inline_buf = []

    # Start with element.text
    if element.text:
        inline_buf.append(element.text)

    for child in element:
        if not isinstance(child.tag, str):
            if child.tail:
                inline_buf.append(child.tail)
            continue
        local = etree.QName(child).localname
        if local in BLOCK_TAGS:
            # Close current inline paragraph
            flush_inline()
            # Add block with surrounding blank lines handled by caller join
            pieces.append(convert_element(child, abs_xml_path, baseline_depth, parent_level))
            # Continue with tail as inline
            if child.tail:
                inline_buf.append(child.tail)
        else:
            # Inline-ish element
            inline_buf.append(convert_inline_like(child, abs_xml_path, baseline_depth, parent_level))
            if child.tail:
                inline_buf.append(child.tail)

    flush_inline()
    return "\n\n".join(filter(None, pieces))

def convert_term(element, abs_xml_path: Path, baseline_depth: int, parent_level: int) -> str:
    """
    Render a DocBook <term> as inline text, preserving inline formatting.
    Avoid introducing block content.
    """
    parts: List[str] = []
    if element.text:
        parts.append(element.text)
    for child in element:
        if not isinstance(child.tag, str):
            if child.tail:
                parts.append(child.tail)
            continue
        local = etree.QName(child).localname
        if local in BLOCK_TAGS:
            # Degrade gracefully: use plain text from the block
            parts.append(" ".join(child.itertext()).strip())
        else:
            parts.append(convert_inline_like(child, abs_xml_path, baseline_depth, parent_level))
        if child.tail:
            parts.append(child.tail)
    return " ".join(" ".join(parts).split()).strip()

def convert_element(element, abs_xml_path: Path, baseline_depth: int, parent_level: int) -> str:
    if not isinstance(element.tag, str):
        return ""
    tag_name = etree.QName(element).localname

    # Inline-only simplesect (bold label + content, not a section)
    if tag_name == "simplesect":
        te = element.find("title")
        title = (te.text or "").strip() if te is not None else ""
        title_line = f"*{title}*\n\n" if title else ""
        children = [
            convert_element(child, abs_xml_path, baseline_depth, parent_level)
            for child in element
            if isinstance(child.tag, str) and etree.QName(child).localname != "title"
        ]
        return title_line + "\n\n".join(filter(None, children))

    # Unwrap container-ish nodes
    if tag_name in {"partintro", "refnamediv", "bookinfo", "refmeta", "refsynopsisdiv"}:
        return "\n\n".join(
            filter(None, [
                convert_element(child, abs_xml_path, baseline_depth, parent_level)
                for child in element if isinstance(child.tag, str)
            ])
        )

    # Inline DocBook <part> (if encountered inside a page)
    # Render as a normal section heading and emit plain include lines (depth baked in target files)
    if tag_name == "part":
        te = element.find("title")
        title = (te.text or "").strip() if te is not None else "Untitled"
        elem_id = element.get("id")
        out: List[str] = []
        if elem_id:
            out.append(f"[[{sanitize_id(elem_id)}]]")
        out.append(f"{'=' * (baseline_depth + 1)} {title}")
        out.append("")
        non_include_chunks: List[str] = []
        include_lines: List[str] = []
        for child in element:
            if not isinstance(child.tag, str):
                continue
            if child.tag == f"{{{XI_NS}}}include":
                include_lines.append(convert_element(child, abs_xml_path, baseline_depth, parent_level))
            else:
                local = etree.QName(child).localname
                if local != "title":
                    chunk = convert_element(child, abs_xml_path, baseline_depth, parent_level).strip()
                    if chunk:
                        non_include_chunks.append(chunk)
        if non_include_chunks:
            out.append("\n\n".join(non_include_chunks))
            out.append("")
        if include_lines:
            out.extend(include_lines)
        return "\n".join(out)

    # Structured sections relative to the page baseline
    if tag_name in {"chapter", "appendix", "preface", "reference", "section", "sect1", "sect2", "sect3", "sect4", "sect5"}:
        te = element.find("title")
        title = (te.text or "").strip() if te is not None else "Untitled"
        elem_id = element.get("id")

        doc_level = docbook_next_level(tag_name, parent_level)
        depth = to_depth(baseline_depth, doc_level)

        heading = f"{'=' * max(1, depth)} {title}"
        if elem_id:
            heading = f"[[{sanitize_id(elem_id)}]]\n{heading}"
        if tag_name == "preface":
            heading = f"[preface]\n{heading}"

        children = [
            convert_element(child, abs_xml_path, baseline_depth, doc_level)
            for child in element
            if isinstance(child.tag, str) and etree.QName(child).localname != "title"
        ]
        return f"{heading}\n\n" + "\n\n".join(filter(None, children))

    # Reference entry under page baseline
    if tag_name == "refentry":
        title_text = "Untitled"
        if (te := element.find(".//refentrytitle")) is not None and (t := (te.text or "").strip()):
            title_text = t
        elif (ne := element.find(".//refname")) is not None and (n := (ne.text or "").strip()):
            title_text = n

        purpose_text = ""
        if (pe := element.find(".//refpurpose")) is not None and (p := (pe.text or "").strip()):
            purpose_text = p

        elem_id = element.get("id")
        depth = to_depth(baseline_depth, docbook_next_level("refentry", parent_level))
        heading = f"{'=' * max(1, depth)} {title_text}"
        if elem_id:
            heading = f"[[{sanitize_id(elem_id)}]]\n{heading}"

        children = [
            convert_element(child, abs_xml_path, baseline_depth, parent_level + 1)
            for child in element
            if isinstance(child.tag, str) and etree.QName(child).localname not in {"refmeta", "refnamediv"}
        ]
        body = "\n\n".join(filter(None, children))
        return f"{heading}\n\n{purpose_text}\n\n{body}".strip()

    # Formal paragraph (titled paragraph)
    if tag_name == "formalpara":
        title_text = ""
        if (te := element.find("title")) is not None and (t := (te.text or "").strip()):
            title_text = t
        body_chunks: List[str] = []
        for child in element:
            if not isinstance(child.tag, str):
                continue
            local = etree.QName(child).localname
            if local == "title":
                continue
            body = convert_element(child, abs_xml_path, baseline_depth, parent_level).strip()
            if body:
                body_chunks.append(body)
        body_text = "\n\n".join(body_chunks)
        return f"*{title_text}*\n\n{body_text}" if title_text else body_text

    # Paragraphs with block-preserving behavior
    if tag_name == "para":
        return convert_para(element, abs_xml_path, baseline_depth, parent_level)

    # Blocks and inline
    if tag_name in {"figure", "informalfigure"}:
        return convert_figure(element, abs_xml_path)

    if tag_name in {"screen", "programlisting"}:
        lang = element.get("language", "")
        hdr = f"[source,{lang}]\n" if lang else ""
        code = etree.tostring(element, method="text", encoding="unicode").strip()
        return f"{hdr}----\n{code}\n----"

    if tag_name in {"table", "informaltable"}:
        title = ""
        if (te := element.find("title")) is not None and (t := (te.text or "").strip()):
            title = f".{t}"
        return f"{title}\n{convert_xml_snippet(element)}"

    if tag_name in {"itemizedlist", "orderedlist"}:
        # Use list continuation '+' (no open block). Ensure adjacency: no extra blank lines
        # around '+'; place a blank line between sibling items for robustness.
        marker = "*" if tag_name == "itemizedlist" else "."
        items: List[str] = []
        for li in element.findall("listitem"):
            li_chunks: List[str] = []
            for child in li:
                if not isinstance(child.tag, str):
                    continue
                chunk = convert_element(child, abs_xml_path, baseline_depth, parent_level).strip()
                if chunk:
                    li_chunks.append(chunk)

            if not li_chunks:
                text = " ".join("".join(li.itertext()).split())
                items.append(f"{marker} {text}")
                continue

            # First chunk after the marker
            item_text = f"{marker} {li_chunks[0]}"
            # Attach any subsequent blocks with a single continuation each, tightly
            for extra in li_chunks[1:]:
                item_text += "\n+\n" + extra
            items.append(item_text)

        # Add a blank line between list items to avoid parser edge cases with continuations
        return "\n\n".join(items)

    if tag_name == "variablelist":
        out: List[str] = []

        # Handle title if present
        if (te := element.find("title")) is not None and (t := (te.text or "").strip()):
            out.append(f".{t}")

        # Separate formalpara and figure elements from varlistentry elements
        formalpara_content: List[str] = []
        figure_content: List[str] = []
        varlist_entries: List[etree._Element] = []

        for child in element:
            if not isinstance(child.tag, str):
                continue
            child_tag = etree.QName(child).localname

            if child_tag == "formalpara":
                content = convert_element(child, abs_xml_path, baseline_depth, parent_level).strip()
                if content:
                    formalpara_content.append(content)
            elif child_tag in {"figure", "informalfigure"}:
                content = convert_element(child, abs_xml_path, baseline_depth, parent_level).strip()
                if content:
                    figure_content.append(content)
            elif child_tag == "varlistentry":
                varlist_entries.append(child)

        # Add formalpara content before the variable list
        if formalpara_content:
            out.extend(formalpara_content)
            out.append("")  # Add blank line before variable list

        # Add horizontal style for two-column layout if we have entries
        if varlist_entries:
            out.append("[horizontal]")

        # Process variable list entries
        for entry in varlist_entries:
            # Collect all terms for this entry and join them with " / "
            terms: List[str] = []
            for term in entry.findall("term"):
                term_content = convert_term(term, abs_xml_path, baseline_depth, parent_level).strip()
                if term_content:
                    terms.append(term_content)

            if terms:
                # Join multiple terms with " / " and add the :: marker
                out.append(f"{' / '.join(terms)}::")

            if (listitem := entry.find("listitem")) is not None:
                # Handle listitem content properly
                listitem_pieces: List[str] = []
                for child in listitem:
                    if not isinstance(child.tag, str):
                        continue
                    child_content = convert_element(child, abs_xml_path, baseline_depth, parent_level).strip()
                    if child_content:
                        listitem_pieces.append(child_content)

                if not listitem_pieces:
                    # Fallback to direct text content
                    fallback = " ".join(" ".join(listitem.itertext()).split()).strip()
                    if fallback:
                        listitem_pieces.append(fallback)

                if listitem_pieces:
                    body = "\n\n".join(listitem_pieces)
                    # For horizontal layout, indent with 4 spaces so it renders as the definition
                    indented_lines: List[str] = []
                    for line in body.split('\n'):
                        if line.strip():
                            indented_lines.append(f"    {line}")
                        else:
                            indented_lines.append("")
                    out.append("\n".join(indented_lines))

        # Add figure content after the variable list
        if figure_content:
            out.append("")  # Add blank line after variable list
            out.extend(figure_content)

        return "\n".join(filter(None, out))

    if tag_name in {"note", "important", "warning", "tip", "caution"}:
        # No leading/trailing blank lines; keep it tight so '+'
        # can directly precede/follow this block inside list items.
        content = convert_para(element, abs_xml_path, baseline_depth, parent_level).strip()
        return f"[{tag_name.upper()}]\n====\n{content}\n===="

    if tag_name in {"refsect1", "refsect2", "refsect3"}:
        te = element.find("title")
        title = (te.text or "").strip() if te is not None else ""
        body = convert_para(element, abs_xml_path, baseline_depth, parent_level)
        return f".{title}\n{body}" if title else body

    if tag_name == "funcsynopsis":
        text_content = re.sub(r"\n\s*\n", "\n", etree.tostring(element, method="text", encoding="unicode").strip())
        lang = "fortran" if "SUBROUTINE" in text_content.upper() else "c"
        return f"[source,{lang}]\n----\n{text_content}\n----"

    if tag_name == "cmdsynopsis":
        parts = []
        for item in element:
            if not isinstance(item.tag, str):
                continue
            child_name = etree.QName(item).localname
            text = "".join(item.itertext()).strip()
            if child_name == "command":
                parts.append(f"*{text}*")
            elif child_name == "arg":
                rep = item.find(".//replaceable")
                arg_text = f"<{rep.text.strip()}>" if rep is not None and rep.text else text
                parts.append(f"[{arg_text}]" if item.get("choice") == "opt" else arg_text)
        return f'[source, subs="+quotes"]\n----\n{" ".join(parts)}\n----'

    if tag_name == "listitem":
        return convert_para(element, abs_xml_path, baseline_depth, parent_level)

    # Inline styles (fallbacks used by convert_inline_like, too)
    if tag_name in {"literal", "command", "function", "option", "parameter", "filename"}:
        return f"`{''.join(element.itertext()).strip()}`"
    if tag_name == "emphasis":
        inner = "".join(element.itertext()).strip()
        return f"*{inner}*" if element.get("role") == "bold" else f"_{inner}_"
    if tag_name == "firstterm":
        return f"_{''.join(element.itertext()).strip()}_"
    if tag_name in {"xref", "link"}:
        if linkend := element.get("linkend"):
            return f"<<{sanitize_id(linkend)}>>"
        return ""
    if tag_name == "ulink":
        url = element.get("url")
        text = "".join(element.itertext()).strip()
        return f"link:{url}[{text or url}]"

    # XInclude => plain include:: target (no leveloffset)
    if element.tag == f"{{{XI_NS}}}include":
        href = element.get("href")
        include_path = (abs_xml_path.parent / href).resolve()
        if not include_path.exists():
            return f"// ERROR: INCLUDE NOT FOUND: {href}"
        rel_include_path = include_path.relative_to(ORIGINAL_SRC_DIR)
        adoc_target_path = (PAGES_DIR / rel_include_path).with_suffix(".adoc")
        current_dir = (PAGES_DIR / abs_xml_path.relative_to(ORIGINAL_SRC_DIR)).parent
        rel_path = os.path.relpath(adoc_target_path, current_dir)
        return f"include::{rel_path}[]"

    if tag_name == "title":
        return ""

    # Fallback
    print(f" -> WARNING: Using Pandoc fallback for tag '{tag_name}' in {abs_xml_path.name}")
    return convert_xml_snippet(element)

def process_xml_file(xml_path: Path, depth_map: Dict[Path, int]):
    """Convert a DocBook XML file into an AsciiDoc page with baked-in heading depth."""
    if xml_path in PROCESSED_FILES:
        return
    print(f"Processing: {xml_path.relative_to(ORIGINAL_SRC_DIR)}")
    PROCESSED_FILES.add(xml_path)

    rel = xml_path.relative_to(ORIGINAL_SRC_DIR)
    out_path = (PAGES_DIR / rel).with_suffix(".adoc")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        root = etree.fromstring(xml_path.read_bytes(), parser=etree.XMLParser(recover=True, no_network=True))
    except etree.XMLSyntaxError as e:
        print(f"FATAL: XML parsing failed for {xml_path}. Error: {e}")
        raise

    root_tag = etree.QName(root).localname
    title_element = root.find("title")
    is_master = xml_path.name in MASTER_FILES

    # Compute baked top heading depth:
    # depth 0 => "=", 1 => "==", 2 => "===", ...
    page_depth = 0 if is_master else depth_map.get(xml_path, 1)
    start_equals = 1 + page_depth

    with open(out_path, "w", encoding="utf-8") as f:
        # Root simplesect => inline only (no page title)
        if root_tag == "simplesect":
            content = convert_element(root, xml_path, baseline_depth=start_equals, parent_level=1)
            f.write(content.strip() + "\n")
            return

        # Page title
        title_text = (title_element.text or "").strip() if title_element is not None else ""
        if title_text:
            elem_id = root.get("id")
            heading = f"{'=' * start_equals} {title_text}"
            if elem_id:
                heading = f"[[{sanitize_id(elem_id)}]]\n{heading}"
            f.write(heading + "\n")
            if is_master:
                f.write(":doctype: book\n")
            f.write("\n")  # end of header block

            if is_master:
                # Shared attributes after header (e.g., sectnums, toclevels, theme)
                f.write("include::../../partials/_header.adoc[]\n\n")

        # Convert children relative to this page's baseline
        children = [
            convert_element(c, xml_path, baseline_depth=start_equals, parent_level=1)
            for c in root
            if isinstance(c.tag, str) and etree.QName(c).localname not in {"title", "bookinfo"}
        ]
        f.write("\n\n".join(filter(None, children)))
        f.write("\n")