#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt


def run_pandoc(input_md: Path, output_docx: Path) -> None:
    cmd = [
        "pandoc",
        str(input_md),
        "-f",
        "gfm",
        "-t",
        "docx",
        "-s",
        "--resource-path",
        str(input_md.parent.resolve()),
        "-o",
        str(output_docx),
    ]
    subprocess.run(cmd, check=True)


def ensure_style(document: Document, style_name: str, style_type=WD_STYLE_TYPE.PARAGRAPH):
    for style in document.styles:
        if style.name == style_name:
            return style
    return document.styles.add_style(style_name, style_type)


def add_page_number(paragraph):
    run = paragraph.add_run()
    fld_char_begin = OxmlElement("w:fldChar")
    fld_char_begin.set(qn("w:fldCharType"), "begin")

    instr_text = OxmlElement("w:instrText")
    instr_text.set(qn("xml:space"), "preserve")
    instr_text.text = "PAGE"

    fld_char_end = OxmlElement("w:fldChar")
    fld_char_end.set(qn("w:fldCharType"), "end")

    run._r.append(fld_char_begin)
    run._r.append(instr_text)
    run._r.append(fld_char_end)


def set_run_font(run, name="Times New Roman", size=None, bold=None, italic=None):
    run.font.name = name
    if run._element.rPr is None:
        run._element.get_or_add_rPr()
    run._element.rPr.rFonts.set(qn("w:ascii"), name)
    run._element.rPr.rFonts.set(qn("w:hAnsi"), name)
    if size is not None:
        run.font.size = Pt(size)
    if bold is not None:
        run.font.bold = bold
    if italic is not None:
        run.font.italic = italic


def set_style_font(style, name="Times New Roman", size=11, bold=False, italic=False):
    style.font.name = name
    style._element.rPr.rFonts.set(qn("w:ascii"), name)
    style._element.rPr.rFonts.set(qn("w:hAnsi"), name)
    style.font.size = Pt(size)
    style.font.bold = bold
    style.font.italic = italic


def postprocess_docx(output_docx: Path, title_text: str) -> None:
    doc = Document(str(output_docx))

    for section in doc.sections:
        section.start_type = WD_SECTION.NEW_PAGE
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

        footer = section.footer
        p = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.clear()
        p.add_run("Page ")
        add_page_number(p)

    set_style_font(doc.styles["Normal"], size=11)
    set_style_font(doc.styles["Title"], size=18, bold=True)
    set_style_font(doc.styles["Heading 1"], size=16, bold=True)
    set_style_font(doc.styles["Heading 2"], size=14, bold=True)
    set_style_font(doc.styles["Heading 3"], size=12, bold=True)

    caption = ensure_style(doc, "Caption")
    set_style_font(caption, size=10, italic=True)

    first_nonempty = None
    for p in doc.paragraphs:
        if p.text.strip():
            first_nonempty = p
            break

    if first_nonempty is not None:
        first_nonempty.style = doc.styles["Title"]
        first_nonempty.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in first_nonempty.runs:
            set_run_font(r, size=18, bold=True)

    for p in doc.paragraphs:
        txt = p.text.strip()
        if not txt:
            continue
        if txt.startswith("Figure ") or txt.startswith("Table "):
            p.style = caption
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        elif txt == "Abstract":
            p.style = doc.styles["Heading 1"]
        elif p.style.name == "Normal":
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.line_spacing = 1.15
        for r in p.runs:
            set_run_font(r, size=11 if p.style.name == "Normal" else None)

    doc.core_properties.title = title_text
    doc.core_properties.subject = "Converted from markdown"
    doc.core_properties.author = "Hermes Agent"
    doc.save(str(output_docx))


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert markdown to styled DOCX via pandoc + python-docx.")
    parser.add_argument("input_md", help="Input markdown file")
    parser.add_argument("output_docx", help="Output docx path")
    args = parser.parse_args()

    input_md = Path(args.input_md).resolve()
    output_docx = Path(args.output_docx).resolve()
    output_docx.parent.mkdir(parents=True, exist_ok=True)

    run_pandoc(input_md, output_docx)
    postprocess_docx(output_docx, title_text=input_md.stem.replace("_", " "))
    print(output_docx)


if __name__ == "__main__":
    main()
