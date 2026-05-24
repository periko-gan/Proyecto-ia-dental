from __future__ import annotations
import re
from pathlib import Path
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt

MD_PATH = Path(__file__).resolve().parents[1] / 'DOCUMENTACION_PROYECTO.md'
OUT_DOCX = Path(__file__).resolve().parents[1] / 'DOCUMENTACION_PROYECTO.docx'


def insert_toc(document: Document):
    """Insert a Table of Contents field in the document."""
    p = document.add_paragraph()
    fld = OxmlElement('w:fldSimple')
    fld.set(qn('w:instr'), 'TOC \\o "1-3" \\h \\z \\u')
    p._p.append(fld)


def add_code_paragraph(document: Document, code_lines: list[str]):
    p = document.add_paragraph()
    run = p.add_run('\n'.join(code_lines))
    run.font.name = 'Courier New'
    run.font.size = Pt(9)


def md_to_docx(md_path: Path, out_path: Path) -> None:
    with md_path.open(encoding='utf-8') as f:
        lines = f.readlines()

    doc = Document()
    first_heading_seen = False
    in_code = False
    code_buffer: list[str] = []

    for raw in lines:
        line = raw.rstrip('\n')
        if line.strip().startswith('```'):
            in_code = not in_code
            if not in_code and code_buffer:
                add_code_paragraph(doc, code_buffer)
                code_buffer = []
            continue
        if in_code:
            code_buffer.append(line)
            continue

        # Heading
        m = re.match(r'^(#{1,6})\s+(.*)', line)
        if m:
            level = len(m.group(1))
            text = m.group(2).strip()
            # Use heading style compatible with python-docx (level 1..9)
            if level > 6:
                level = 6
            # If this is first top-level heading, add as title and then insert TOC
            if level == 1 and not first_heading_seen:
                doc.add_heading(text, level=1)
                insert_toc(doc)
                first_heading_seen = True
            else:
                doc.add_heading(text, level=level)
            continue

        # Horizontal rule
        if re.match(r'^---+$', line.strip()):
            doc.add_page_break()
            continue

        # Lists (simple unordered)
        mlist = re.match(r'^\s*[-\*+]\s+(.*)', line)
        if mlist:
            doc.add_paragraph(mlist.group(1), style='List Bullet')
            continue

        # Ordered list
        mold = re.match(r'^\s*\d+[\.)]\s+(.*)', line)
        if mold:
            doc.add_paragraph(mold.group(1), style='List Number')
            continue

        # Tables or block with pipes: add as preformatted text
        if '|' in line and re.match(r'\s*\|?.+\|.+', line):
            p = doc.add_paragraph(line)
            continue

        # Empty line
        if line.strip() == '':
            doc.add_paragraph('')
            continue

        # Normal paragraph
        doc.add_paragraph(line)

    # If code block still open
    if code_buffer:
        add_code_paragraph(doc, code_buffer)

    doc.save(out_path)
    print(f'Wrote: {out_path}')


if __name__ == '__main__':
    if not MD_PATH.exists():
        print('Markdown source not found:', MD_PATH)
    else:
        md_to_docx(MD_PATH, OUT_DOCX)

