#!/usr/bin/env python3
"""
finalize.py — turn Hannah's f1r3lang directory into a deployable GitHub Pages site.

    python3 deploy/finalize.py f1r3lang.ai --site f1r3lang

Idempotent: run it again after any content edit and it will rewrite, not duplicate.

What it writes
  .nojekyll     stops GitHub running Jekyll. REQUIRED — developers.html contains
                <code>{% P %}[s]</code>, which Liquid reads as an unknown tag and
                fails the build on.
  CNAME         the custom domain, one hostname, no scheme
  404.html      a not-found page in the site's own type and colour
  robots.txt    allow all, point at the sitemap
  sitemap.xml   the six pages, with lastmod from the file mtimes
  <link rel="canonical">, og:url, og:site_name, and a favicon link, inserted
                into every page's <head>

What it does NOT do
  Nothing to Hannah's markup below <head>. No reformatting, no link rewriting —
  every path in the site is already relative, so it relocates as-is.
"""

import argparse
import datetime
import pathlib
import re
import sys

PAGES = {
    "index.html": ("f1r3lang", 1.0),
    "language.html": ("The Language", 0.9),
    "get-started.html": ("Get Started", 0.9),
    "research.html": ("Research", 0.8),
    "ecosystem.html": ("Ecosystem", 0.7),
    "developers.html": ("f1r3lang for the Working Software Developer", 0.8),
}

MARK_OPEN = "  <!-- deploy:begin (finalize.py — do not hand-edit) -->"
MARK_CLOSE = "  <!-- deploy:end -->"

NOT_FOUND = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Not found &mdash; f1r3lang</title>
  <meta name="robots" content="noindex">
  <meta name="theme-color" content="#0A0A0A">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Josefin+Sans:wght@300;400;600;700&family=Source+Sans+3:wght@300;400;600&family=JetBrains+Mono:wght@400;700&display=swap">
  <link rel="stylesheet" href="/css/styles.css">
</head>
<body>

<nav class="site-nav" aria-label="Main navigation">
  <div class="nav-container">
    <a href="/index.html" class="nav-logo">
      <img src="/images/f1r3lang-logo-v1.svg" alt="f1r3lang">
    </a>
  </div>
</nav>

<main id="main">
  <section class="section">
    <div class="section-header">
      <p class="eyebrow">404</p>
      <h1>No such page</h1>
      <div class="section-rule"></div>
    </div>
    <div class="prose">
      <p>That address does not name anything here. The channel exists; nothing is
      listening on it.</p>
      <p><a href="/index.html">Home</a> &middot;
         <a href="/language.html">The Language</a> &middot;
         <a href="/get-started.html">Get Started</a> &middot;
         <a href="/research.html">Research</a> &middot;
         <a href="/ecosystem.html">Ecosystem</a></p>
    </div>
  </section>
</main>

<footer class="site-footer">
  <div class="footer-container">
    <div class="footer-brand">
      <img src="/images/f1r3lang-logo-v1.svg" alt="">
      <span class="footer-note">A <a href="https://f1r3fly.io" target="_blank" rel="noopener">F1R3FLY</a> language</span>
    </div>
    <span class="footer-copy">&copy; F1R3FLY INDUSTRIES, 2026. All Rights Reserved</span>
  </div>
</footer>

</body>
</html>
"""


def patch(path, domain, page, title):
    html = path.read_text(encoding="utf-8")

    # drop any previous run's block
    html = re.sub(
        re.escape(MARK_OPEN) + r".*?" + re.escape(MARK_CLOSE) + r"\n?",
        "",
        html,
        flags=re.S,
    )
    # drop hand-written og:url / og:type, so we don't emit two of each
    html = re.sub(r'\n\s*<meta property="og:(?:url|type)"[^>]*>', "", html)

    url = f"https://{domain}/" if page == "index.html" else f"https://{domain}/{page}"
    lines = [
        MARK_OPEN,
        f'  <link rel="canonical" href="{url}">',
        '  <link rel="icon" href="/images/f1r3lang-logo-v1.svg" type="image/svg+xml">',
        f'  <meta property="og:url" content="{url}">',
        '  <meta property="og:site_name" content="f1r3lang">',
        '  <meta property="og:type" content="website">',
    ]
    # Hannah hand-wrote og:title and og:description on the home page. Only supply
    # them where they are missing; never duplicate.
    if 'property="og:title"' not in html:
        lines.append(f'  <meta property="og:title" content="{title}">')
    if 'property="og:description"' not in html:
        m = re.search(r'<meta name="description" content="([^"]*)"', html)
        if m:
            lines.append(f'  <meta property="og:description" content="{m.group(1)}">')
    lines.append(MARK_CLOSE)

    if "</head>" not in html:
        sys.exit(f"{path}: no </head>")
    html = html.replace("</head>", "\n".join(lines) + "\n</head>", 1)
    path.write_text(html, encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("domain", help="canonical hostname, e.g. f1r3lang.ai")
    ap.add_argument("--site", default="f1r3lang", help="path to the site directory")
    ap.add_argument("--drop-rholang-logos", action="store_true",
                    help="delete the three legacy rholang-logo-*.svg files")
    args = ap.parse_args()

    root = pathlib.Path(args.site).resolve()
    if not (root / "index.html").exists():
        sys.exit(f"{root}: no index.html — wrong --site?")

    domain = args.domain.strip().lower().removeprefix("https://").removeprefix("http://").rstrip("/")

    (root / ".nojekyll").write_text("")
    (root / "CNAME").write_text(domain + "\n")
    (root / "404.html").write_text(NOT_FOUND, encoding="utf-8")
    (root / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: https://{domain}/sitemap.xml\n"
    )

    urls = []
    for page, (title, priority) in PAGES.items():
        f = root / page
        if not f.exists():
            print(f"  skip (absent): {page}")
            continue
        patch(f, domain, page, title)
        lastmod = datetime.date.fromtimestamp(f.stat().st_mtime).isoformat()
        loc = f"https://{domain}/" if page == "index.html" else f"https://{domain}/{page}"
        urls.append(f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{lastmod}</lastmod>\n"
                    f"    <priority>{priority}</priority>\n  </url>")
        print(f"  patched: {page}")

    (root / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls) + "\n</urlset>\n"
    )

    if args.drop_rholang_logos:
        for f in (root / "images").glob("rholang-logo-*.svg"):
            f.unlink()
            print(f"  removed: images/{f.name}")

    print(f"\n{root} is ready for {domain}")
    print("  wrote .nojekyll, CNAME, 404.html, robots.txt, sitemap.xml")


if __name__ == "__main__":
    main()
