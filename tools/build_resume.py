"""Build the ATS-friendly resume DOCX (editable source).

Run from the project root:
    python tools/build_resume.py

Requires python-docx (pip install python-docx).
Content lives in tools/resume_content.py.
"""

from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

import resume_content as C

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "Ayush_Patel_Resume.docx"

INK = RGBColor(0x11, 0x18, 0x27)
BODY = RGBColor(0x1F, 0x29, 0x37)
MUTED = RGBColor(0x4B, 0x55, 0x63)


def set_character_spacing(run, points):
    spacing = OxmlElement("w:spacing")
    spacing.set(qn("w:val"), str(int(points * 20)))
    run._element.get_or_add_rPr().append(spacing)


def add_bottom_border(paragraph, color="C9D2DC", size="6"):
    p_pr = paragraph._p.get_or_add_pPr()
    borders = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), size)
    bottom.set(qn("w:space"), "2")
    bottom.set(qn("w:color"), color)
    borders.append(bottom)
    p_pr.append(borders)


def configure(document):
    section = document.sections[0]
    section.page_width = Inches(8.27)
    section.page_height = Inches(11.69)
    section.top_margin = Inches(0.55)
    section.bottom_margin = Inches(0.55)
    section.left_margin = Inches(0.6)
    section.right_margin = Inches(0.6)

    normal = document.styles["Normal"]
    normal.font.name = "Calibri"
    normal.font.size = Pt(9.8)
    normal.font.color.rgb = BODY
    normal.paragraph_format.space_before = Pt(0)
    normal.paragraph_format.space_after = Pt(2)
    normal.paragraph_format.line_spacing = 1.0

    rpr = normal.element.get_or_add_rPr()
    fonts = rpr.find(qn("w:rFonts"))
    if fonts is None:
        fonts = OxmlElement("w:rFonts")
        rpr.append(fonts)
    for attribute in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        fonts.set(qn(attribute), "Calibri")


def section_heading(document, text):
    paragraph = document.add_paragraph()
    paragraph.paragraph_format.space_before = Pt(9)
    paragraph.paragraph_format.space_after = Pt(4)
    paragraph.paragraph_format.keep_with_next = True
    run = paragraph.add_run(text.upper())
    run.bold = True
    run.font.size = Pt(9.6)
    run.font.color.rgb = INK
    set_character_spacing(run, 0.8)
    add_bottom_border(paragraph)


def entry(document, title, meta):
    title_paragraph = document.add_paragraph()
    title_paragraph.paragraph_format.space_before = Pt(4)
    title_paragraph.paragraph_format.space_after = Pt(0)
    title_paragraph.paragraph_format.keep_with_next = True
    title_run = title_paragraph.add_run(title)
    title_run.bold = True
    title_run.font.size = Pt(10.4)
    title_run.font.color.rgb = INK

    meta_paragraph = document.add_paragraph()
    meta_paragraph.paragraph_format.space_before = Pt(0)
    meta_paragraph.paragraph_format.space_after = Pt(2)
    meta_paragraph.paragraph_format.keep_with_next = True
    meta_run = meta_paragraph.add_run(meta)
    meta_run.italic = True
    meta_run.font.size = Pt(9)
    meta_run.font.color.rgb = MUTED


def bullet(document, text):
    paragraph = document.add_paragraph(style="List Bullet")
    paragraph.paragraph_format.space_before = Pt(0)
    paragraph.paragraph_format.space_after = Pt(1.4)
    paragraph.paragraph_format.left_indent = Inches(0.22)
    paragraph.paragraph_format.first_line_indent = Inches(-0.16)
    run = paragraph.add_run(text)
    run.font.size = Pt(9.6)


def body_line(document, label, value):
    paragraph = document.add_paragraph()
    paragraph.paragraph_format.space_before = Pt(0)
    paragraph.paragraph_format.space_after = Pt(2)
    label_run = paragraph.add_run(label + ": ")
    label_run.bold = True
    label_run.font.size = Pt(9.6)
    label_run.font.color.rgb = INK
    value_run = paragraph.add_run(value)
    value_run.font.size = Pt(9.6)


def build():
    document = Document()
    configure(document)

    core = document.core_properties
    core.author = "Ayush Patel"
    core.title = "Ayush Patel — Backend Software Engineer"
    core.subject = "Resume — Backend Software Engineer, Python, Django, REST APIs, PostgreSQL"
    core.keywords = (
        "Backend Software Engineer, Python, Django, Django REST Framework, REST APIs, "
        "PostgreSQL, SQL Server, Docker, RAG, LLM"
    )
    core.comments = "ATS-friendly resume generated from tools/resume_content.py"

    # Header
    name = document.add_paragraph()
    name.paragraph_format.space_after = Pt(1)
    name_run = name.add_run(C.NAME)
    name_run.bold = True
    name_run.font.size = Pt(20)
    name_run.font.color.rgb = INK
    set_character_spacing(name_run, 0.6)

    for text, size, colour in (
        (C.HEADLINE, 10.2, BODY),
        (C.CONTACT, 9, MUTED),
        (C.LINKS, 9, MUTED),
    ):
        paragraph = document.add_paragraph()
        paragraph.paragraph_format.space_after = Pt(1)
        run = paragraph.add_run(text)
        run.font.size = Pt(size)
        run.font.color.rgb = colour

    # Summary
    section_heading(document, "Professional Summary")
    summary = document.add_paragraph()
    summary.paragraph_format.space_after = Pt(0)
    summary_run = summary.add_run(C.SUMMARY)
    summary_run.font.size = Pt(9.6)

    # Experience
    section_heading(document, "Experience")
    for role in C.EXPERIENCE:
        entry(document, role["title"], role["meta"])
        for text in role["bullets"]:
            bullet(document, text)

    # Projects
    section_heading(document, "Projects")
    for project in C.PROJECTS:
        entry(document, project["title"], project["tech"])
        for text in project["bullets"]:
            bullet(document, text)

    # Skills
    section_heading(document, "Technical Skills")
    for label, value in C.SKILLS:
        body_line(document, label, value)

    # Education
    section_heading(document, "Education")
    for item in C.EDUCATION:
        entry(document, item["title"], item["meta"])

    # Certifications
    section_heading(document, "Certifications")
    for text in C.CERTIFICATIONS:
        bullet(document, text)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    document.save(OUT)
    print(f"Saved {OUT}")


if __name__ == "__main__":
    build()
