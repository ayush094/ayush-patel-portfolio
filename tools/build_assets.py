"""Generate the portfolio's image assets.

Run from the project root:
    python tools/build_assets.py

Requires Pillow (pip install pillow).
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

BG = (10, 14, 19)
TEXT = (233, 239, 247)
MUTED = (169, 183, 198)
DIM = (127, 142, 158)
ACCENT = (61, 220, 151)

FONT_BOLD = r"C:\Windows\Fonts\segoeuib.ttf"
FONT_REGULAR = r"C:\Windows\Fonts\segoeui.ttf"
FONT_MONO = r"C:\Windows\Fonts\consola.ttf"


def optimize_portrait() -> None:
    source = ASSETS / "profile.jpg"
    image = Image.open(source).convert("RGB")
    target_w = 760
    target_h = round(target_w * 3 / 2)
    image = image.resize((target_w, target_h), Image.LANCZOS)
    image.save(source, "JPEG", quality=86, optimize=True, progressive=True)
    print(f"profile.jpg -> {target_w}x{target_h}, {source.stat().st_size // 1024} KB")


def optimize_preview() -> None:
    source = ASSETS / "shree-krishna-preview.png"
    image = Image.open(source)
    if image.mode in ("RGBA", "LA", "P"):
        background = Image.new("RGB", image.size, (11, 18, 25))
        image = image.convert("RGBA")
        background.paste(image, mask=image.split()[-1])
        image = background
    else:
        image = image.convert("RGB")

    image = image.resize((900, 450), Image.LANCZOS)
    image.save(ASSETS / "shree-krishna-preview.png", "PNG", optimize=True)
    image.save(ASSETS / "shree-krishna-preview.webp", "WEBP", quality=82, method=6)

    png_kb = (ASSETS / "shree-krishna-preview.png").stat().st_size // 1024
    webp_kb = (ASSETS / "shree-krishna-preview.webp").stat().st_size // 1024
    print(f"preview -> 900x450, png {png_kb} KB, webp {webp_kb} KB")


def draw_favicon() -> None:
    size = 512
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((8, 8, size - 8, size - 8), radius=110, fill=BG, outline=ACCENT, width=10)

    font = ImageFont.truetype(FONT_BOLD, 230)
    text = "AP"
    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
    draw.text(
        ((size - (right - left)) / 2 - left, (size - (bottom - top)) / 2 - top - 8),
        text,
        font=font,
        fill=TEXT,
    )
    draw.ellipse((size - 150, size - 150, size - 110, size - 110), fill=ACCENT)

    for filename, size in (
        ("favicon-32.png", 32),
        ("apple-touch-icon.png", 180),
        ("favicon.png", 192),
    ):
        resized = image.resize((size, size), Image.LANCZOS)
        resized.save(ASSETS / filename, "PNG", optimize=True)

    print("favicon-32.png / apple-touch-icon.png / favicon.png generated")


def draw_og_image() -> None:
    width, height = 1200, 630
    image = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(image)

    # faint grid
    for x in range(0, width, 60):
        draw.line([(x, 0), (x, height)], fill=(17, 24, 32), width=1)
    for y in range(0, height, 60):
        draw.line([(0, y), (width, y)], fill=(17, 24, 32), width=1)

    # accent wash
    glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    for radius in range(420, 0, -12):
        alpha = int(16 * (1 - radius / 420))
        glow_draw.ellipse((980 - radius, -140 - radius, 980 + radius, -140 + radius), fill=ACCENT + (alpha,))
    image = Image.alpha_composite(image.convert("RGBA"), glow).convert("RGB")
    draw = ImageDraw.Draw(image)

    draw.rectangle((0, 0, width, 6), fill=ACCENT)

    mono = ImageFont.truetype(FONT_MONO, 24)
    bold = ImageFont.truetype(FONT_BOLD, 76)
    sub = ImageFont.truetype(FONT_REGULAR, 30)
    small = ImageFont.truetype(FONT_REGULAR, 24)

    draw.text((80, 108), "AYUSH PATEL", font=mono, fill=ACCENT)
    draw.text((80, 168), "Backend Software", font=bold, fill=TEXT)
    draw.text((80, 254), "Engineer", font=bold, fill=TEXT)
    draw.text((80, 372), "Python  ·  Django  ·  REST APIs  ·  PostgreSQL", font=sub, fill=MUTED)
    draw.text((80, 424), "RAG and LLM-powered backend systems", font=sub, fill=DIM)

    draw.line((80, 512, 1120, 512), fill=(32, 44, 58), width=2)
    draw.text((80, 540), "buildwithayush.in", font=mono, fill=TEXT)
    draw.text((760, 540), "Software Developer @ SrashtaSoft", font=small, fill=DIM)

    image.save(ASSETS / "og-image.png", "PNG", optimize=True)
    print("og-image.png -> 1200x630")


if __name__ == "__main__":
    optimize_portrait()
    optimize_preview()
    draw_favicon()
    draw_og_image()
