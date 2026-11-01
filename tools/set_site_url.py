"""Point the whole project at a new public URL.

Usage (run from the project root):

    python tools/set_site_url.py --check
    python tools/set_site_url.py --dry-run https://buildwithayush.vercel.app
    python tools/set_site_url.py https://buildwithayush.vercel.app
    python tools/set_site_url.py https://buildwithayush.vercel.app --drop-custom-domain

The public URL is written in several places that are easy to miss: the canonical
link, Open Graph / Twitter tags, JSON-LD, the sitemap, robots.txt, the README,
the resume source and the social preview image. This script rewrites all of them
and then rebuilds the generated files.

`CNAME` is deliberately never rewritten: it is a GitHub Pages custom-domain file,
not a website asset. Pass --drop-custom-domain to delete it when you stop using
a custom domain, otherwise GitHub Pages keeps redirecting to a dead host.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent

# Text files that carry the public URL. CNAME is intentionally excluded.
TEXT_FILES = (
    ROOT / "index.html",
    ROOT / "robots.txt",
    ROOT / "sitemap.xml",
    ROOT / "README.md",
    ROOT / "tools" / "resume_content.py",
    ROOT / "tools" / "build_assets.py",
)

CNAME_FILES = (ROOT / "CNAME", ROOT / "docs" / "CNAME")

CANONICAL_RE = re.compile(r'<link rel="canonical" href="(https?://[^/"]+)/?"')


def current_url() -> str:
    """Read the live URL from the canonical tag so the script is re-runnable."""
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    match = CANONICAL_RE.search(html)
    if not match:
        sys.exit("Could not find <link rel=\"canonical\"> in index.html")
    return match.group(1)


def normalise(value: str) -> str:
    value = value.strip().rstrip("/")
    parsed = urlparse(value)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        sys.exit(f"Not a valid http(s) URL: {value}")
    if parsed.path not in ("", "/"):
        sys.exit(f"Expected a bare origin, got a path: {value}")
    return f"{parsed.scheme}://{parsed.netloc}"


def occurrences(text: str, old_url: str, old_host: str) -> int:
    """Count full URLs plus bare hosts, without counting the host twice."""
    full = len(re.findall(re.escape(old_url), text))
    bare = len(re.findall(rf"(?<!//){re.escape(old_host)}", text))
    return full + bare


def rewrite(new_url: str, old_url: str, dry_run: bool) -> dict[str, int]:
    old_host = urlparse(old_url).netloc
    new_host = urlparse(new_url).netloc
    totals: dict[str, int] = {}

    for path in TEXT_FILES:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        before = occurrences(text, old_url, old_host)
        if not before:
            continue
        # Full URL first so the bare-host pass cannot double-rewrite.
        updated = text.replace(old_url, new_url).replace(old_host, new_host)
        totals[str(path.relative_to(ROOT))] = before
        if not dry_run:
            path.write_text(updated, encoding="utf-8", newline="\n")

    return totals


def rebuild() -> None:
    print("\nRebuilding generated files...")
    for script in ("tools/build_resume.py", "tools/build_resume_pdf.py"):
        result = subprocess.run(
            [sys.executable, str(ROOT / script)],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            sys.exit(f"{script} failed:\n{result.stdout}\n{result.stderr}")
        print(f"  {script} -> ok")

    # Only redraw the OG card; a full build_assets run would re-encode the
    # portrait and the project screenshot for no reason.
    sys.path.insert(0, str(ROOT / "tools"))
    import build_assets  # noqa: E402  (path is set above)

    build_assets.draw_og_image()
    print("  assets/og-image.png -> ok")


def drop_custom_domain() -> None:
    print("\nRemoving GitHub Pages custom-domain files:")
    for path in CNAME_FILES:
        if path.exists():
            path.unlink()
            print(f"  deleted {path.relative_to(ROOT)}")
        else:
            print(f"  {path.relative_to(ROOT)} already absent")


def main() -> None:
    parser = argparse.ArgumentParser(description="Point the portfolio at a new URL.")
    parser.add_argument("url", nargs="?", help="new origin, e.g. https://name.vercel.app")
    parser.add_argument("--check", action="store_true", help="show the current URL and references")
    parser.add_argument("--dry-run", action="store_true", help="report changes without writing")
    parser.add_argument(
        "--drop-custom-domain",
        action="store_true",
        help="delete CNAME files so GitHub Pages stops redirecting to a dead domain",
    )
    args = parser.parse_args()

    old_url = current_url()
    print(f"Current public URL: {old_url}")

    if args.check:
        old_host = urlparse(old_url).netloc
        print("\nReferences found:")
        for path in TEXT_FILES:
            if path.exists():
                count = occurrences(path.read_text(encoding="utf-8"), old_url, old_host)
                if count:
                    print(f"  {count:>2}x  {path.relative_to(ROOT)}")
        print("\nCNAME files:")
        for path in CNAME_FILES:
            print(f"  {'present' if path.exists() else 'absent '}  {path.relative_to(ROOT)}")
        return

    if not args.url:
        parser.error("provide a new URL, or use --check")

    new_url = normalise(args.url)
    if new_url == old_url:
        print("URL is unchanged; nothing to rewrite.")
    else:
        print(f"New public URL:     {new_url}")
        changes = rewrite(new_url, old_url, args.dry_run)
        if not changes:
            print("No references needed changing.")
        else:
            label = "Would update" if args.dry_run else "Updated"
            print(f"\n{label}:")
            for name, count in changes.items():
                print(f"  {count:>2}x  {name}")

    if args.drop_custom_domain:
        drop_custom_domain()

    if args.dry_run:
        print("\nDry run: no files written.")
        return

    if new_url != old_url:
        rebuild()

    print("\nDone. Review the diff, then commit and push.")


if __name__ == "__main__":
    main()
