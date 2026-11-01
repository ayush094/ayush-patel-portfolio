"""Build the ATS-friendly resume PDF.

Run from the project root:
    python tools/build_resume_pdf.py

Requires reportlab (pip install reportlab).
Content lives in tools/resume_content.py, shared with the DOCX builder.

Layout notes: single column, standard fonts, no tables, no text boxes and no
graphics, so parsers read the document in a predictable order.
"""

from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    HRFlowable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)

import resume_content as C

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "Ayush_Patel_Resume.pdf"

INK = HexColor("#111827")
BODY = HexColor("#1f2937")
MUTED = HexColor("#4b5563")
RULE = HexColor("#c9d2dc")

BODY_SIZE = 9.6
BODY_LEADING = 12.3

STYLES = {
    "name": ParagraphStyle(
        "name",
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=22,
        textColor=INK,
        spaceAfter=2,
    ),
    "headline": ParagraphStyle(
        "headline",
        fontName="Helvetica",
        fontSize=10.2,
        leading=13,
        textColor=BODY,
        spaceAfter=1,
    ),
    "contact": ParagraphStyle(
        "contact",
        fontName="Helvetica",
        fontSize=9,
        leading=11.6,
        textColor=MUTED,
        spaceAfter=1,
    ),
    "section": ParagraphStyle(
        "section",
        fontName="Helvetica-Bold",
        fontSize=9.6,
        leading=11.5,
        textColor=INK,
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True,
    ),
    "entry": ParagraphStyle(
        "entry",
        fontName="Helvetica-Bold",
        fontSize=10.4,
        leading=12.6,
        textColor=INK,
        spaceBefore=4,
        spaceAfter=0,
        keepWithNext=True,
    ),
    "meta": ParagraphStyle(
        "meta",
        fontName="Helvetica-Oblique",
        fontSize=9,
        leading=11,
        textColor=MUTED,
        spaceBefore=0,
        spaceAfter=2,
        keepWithNext=True,
    ),
    "body": ParagraphStyle(
        "body",
        fontName="Helvetica",
        fontSize=BODY_SIZE,
        leading=BODY_LEADING,
        textColor=BODY,
        alignment=TA_LEFT,
        spaceAfter=1,
    ),
    "bullet": ParagraphStyle(
        "bullet",
        fontName="Helvetica",
        fontSize=BODY_SIZE,
        leading=BODY_LEADING,
        textColor=BODY,
        leftIndent=14,
        bulletIndent=2,
        bulletFontName="Helvetica",
        bulletFontSize=BODY_SIZE,
        spaceAfter=1.4,
    ),
}

RULE_FLOWABLE = HRFlowable(
    width="100%", thickness=0.6, color=RULE, spaceBefore=1, spaceAfter=3
)


def pdf_text(value):
    """Keep the PDF pure ASCII so every ATS parser reads it cleanly."""
    replacements = {
        "\u2014": "-",   # em dash
        "\u2013": "-",   # en dash
        "\u00b7": "|",   # middle dot
        "\u2019": "'",   # right single quote
        "\u201c": '"',
        "\u201d": '"',
        "\u00a0": " ",
    }
    for source, target in replacements.items():
        value = value.replace(source, target)
    return escape(value)


def section(title):
    return [
        Paragraph(escape(title.upper()), STYLES["section"]),
        RULE_FLOWABLE,
    ]


def entry(title, meta):
    return [
        Paragraph(pdf_text(title), STYLES["entry"]),
        Paragraph(pdf_text(meta), STYLES["meta"]),
    ]


def bullets(items):
    return [Paragraph(pdf_text(text), STYLES["bullet"], bulletText="-") for text in items]


def build():
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=A4,
        leftMargin=0.6 * inch,
        rightMargin=0.6 * inch,
        topMargin=0.55 * inch,
        bottomMargin=0.55 * inch,
        title="Ayush Patel — Backend Software Engineer",
        author="Ayush Patel",
        subject="Resume — Python, Django, REST APIs, PostgreSQL",
        keywords="Backend Software Engineer, Python, Django, DRF, REST APIs, PostgreSQL, Docker, RAG",
        creator="tools/build_resume_pdf.py",
    )

    story = [
        Paragraph(pdf_text(C.NAME), STYLES["name"]),
        Paragraph(pdf_text(C.HEADLINE), STYLES["headline"]),
        Paragraph(pdf_text(C.CONTACT), STYLES["contact"]),
        Paragraph(pdf_text(C.LINKS), STYLES["contact"]),
    ]

    story += section("Professional Summary")
    story.append(Paragraph(pdf_text(C.SUMMARY), STYLES["body"]))

    story += section("Experience")
    for role in C.EXPERIENCE:
        story += entry(role["title"], role["meta"])
        story += bullets(role["bullets"])

    story += section("Projects")
    for project in C.PROJECTS:
        story += entry(project["title"], project["tech"])
        story += bullets(project["bullets"])

    story += section("Technical Skills")
    for label, value in C.SKILLS:
        story.append(
            Paragraph(
                f"<b>{pdf_text(label)}:</b> {pdf_text(value)}",
                STYLES["body"],
            )
        )

    story += section("Education")
    for item in C.EDUCATION:
        story += entry(item["title"], item["meta"])

    story += section("Certifications")
    story += bullets(C.CERTIFICATIONS)

    story.append(Spacer(1, 2))
    doc.build(story)
    print(f"Saved {OUT}")


if __name__ == "__main__":
    build()
