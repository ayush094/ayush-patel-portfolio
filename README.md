# Ayush Patel — Portfolio

A single-page, static portfolio for **buildwithayush.in**.
No backend, no framework, no build step: plain HTML, CSS and JavaScript, deployed
directly from this repository with GitHub Pages.

**Positioning:** Backend Software Engineer — Python · Django · REST APIs · PostgreSQL ·
AI-powered systems.

## Stack

| Layer | Choice |
| --- | --- |
| Markup | Semantic HTML5 (`index.html`) |
| Styling | Hand-written CSS with custom properties (`styles.css`) |
| Behaviour | Vanilla JavaScript, no dependencies (`script.js`) |
| Fonts | Inter + JetBrains Mono (Google Fonts) |
| Hosting | GitHub Pages + custom domain (`CNAME`) |

There is no runtime backend and nothing to compile. Pushing to `main` publishes the
site.

## Local preview

### Option 1 — VS Code Live Server (recommended)

The workspace already pins the port to **5502**.

1. Install the **Live Server** extension (VS Code will suggest it from
   `.vscode/extensions.json`).
2. Open the project folder in VS Code.
3. Right-click `index.html` → **Open with Live Server**, or click **Go Live** in the
   status bar.
4. Open <http://127.0.0.1:5502>.

Saving `index.html`, `styles.css` or `script.js` reloads the browser automatically.

### Option 2 — Python one-liner (no extensions)

```powershell
python -m http.server 5502
```

Then open <http://localhost:5502>. Refresh after edits; there is no auto-reload.

### Option 3 — BrowserSync (auto-reload without installing anything)

```powershell
npx browser-sync start --server --port 5502 --files "index.html, styles.css, script.js, assets/**"
```

Use one option only; they all use the same port.

## Project structure

```text
.
├── index.html                     # All page content and metadata
├── styles.css                     # Design tokens, layout, components, responsive rules
├── script.js                      # Nav, active section, scroll reveal
├── 404.html                       # Static not-found page
├── robots.txt
├── sitemap.xml
├── site.webmanifest
├── vercel.json                    # Security headers + asset caching (Vercel only)
├── .vercelignore                  # Keeps local tooling out of Vercel deployments
├── CNAME                          # buildwithayush.in (GitHub Pages only)
├── assets/
│   ├── profile.jpg                # Optimised portrait (760 × 1140)
│   ├── shree-krishna-preview.*    # Project screenshot (WebP + PNG fallback)
│   ├── og-image.png               # Social share card (1200 × 630)
│   ├── favicon.svg / .png
│   ├── apple-touch-icon.png
│   ├── Ayush_Patel_Resume.pdf     # Downloadable, ATS-friendly resume
│   └── Ayush_Patel_Resume.docx    # Editable resume source
└── tools/                         # LOCAL-ONLY helpers, not used by the website
    ├── resume_content.py          # Single source of truth for resume content
    ├── build_resume.py            # Builds the DOCX
    ├── build_resume_pdf.py        # Builds the PDF (ReportLab)
    ├── build_assets.py            # Rebuilds optimised images / OG card / icons
    └── set_site_url.py            # Repoints every URL reference at a new domain
```

`tools/` is optional. GitHub Pages serves it as inert files and `.vercelignore`
excludes it from Vercel; nothing on the site calls
it. It exists so the resume and images can be regenerated consistently.

## Editing the site

- **Text, sections, links:** `index.html`
- **Colours, spacing, typography:** the `:root` block at the top of `styles.css`
- **Interaction:** `script.js`

All content is in the HTML, so it is indexable without JavaScript.

## Updating the resume

The site links directly to `assets/Ayush_Patel_Resume.pdf` (no Google Drive).

Edit `tools/resume_content.py`, then rebuild both formats:

```powershell
python tools/build_resume.py       # -> assets/Ayush_Patel_Resume.docx
python tools/build_resume_pdf.py   # -> assets/Ayush_Patel_Resume.pdf
```

Requirements: `pip install python-docx reportlab`. The PDF is intentionally ASCII-only
with a single column and no tables or graphics, so ATS parsers read it reliably.

To rebuild images (portrait, project screenshot, favicon, OG card):

```powershell
python tools/build_assets.py       # requires Pillow
```

## Deploying

There is no build step, so every host below serves the repository root as-is.
No environment variables, server configuration or database are required.

### Vercel (recommended, free)

1. Go to <https://vercel.com/new> and import `ayush094/ayush-patel-portfolio`.
2. Framework preset: **Other**. Build command: empty. Output directory: `.`
3. Deploy. Every push to `main` then redeploys automatically.
4. Rename the project under **Settings → General** if you want a shorter URL
   (the domain becomes `<project-name>.vercel.app`).

`vercel.json` adds security headers and a one-hour cache on `/assets`, and
`.vercelignore` keeps `tools/`, `docs/`, `.vscode/` and `CNAME` out of the
deployment.

### GitHub Pages (fallback)

1. Commit and push to `main`.
2. GitHub Pages serves the repository root.
3. `CNAME` holds the custom domain. **Delete it if you stop renewing the domain**,
   otherwise Pages redirects every request to the dead host and the site goes dark
   — including the `github.io` fallback.

### Moving to a new URL

The public URL appears in the canonical tag, Open Graph, Twitter, JSON-LD, the
sitemap, `robots.txt`, the README, the resume source and the OG image. Update all
of them at once:

```powershell
python tools/set_site_url.py --check                              # where is it used?
python tools/set_site_url.py --dry-run https://name.vercel.app    # preview changes
python tools/set_site_url.py https://name.vercel.app --drop-custom-domain
```

The last command also rebuilds the resume PDF/DOCX and the OG image, and deletes
both `CNAME` files so GitHub Pages stops redirecting to the old domain.

## Accessibility & quality notes

- Skip link, keyboard-operable mobile menu, visible focus styles.
- Text selection, copy and context menus are not blocked.
- `prefers-reduced-motion` disables animations.
- Images have intrinsic `width`/`height` to avoid layout shift; below-the-fold images
  are lazy-loaded.
- Metadata includes canonical URL, Open Graph, Twitter card, JSON-LD `Person` schema,
  sitemap and robots directives.
