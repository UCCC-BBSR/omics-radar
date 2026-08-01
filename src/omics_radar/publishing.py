from __future__ import annotations

from collections import defaultdict
from datetime import date
from email.utils import format_datetime
from html import escape
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urljoin
from xml.etree import ElementTree

from .database import get_report_entries, list_published_reports


SITE_TITLE = "BBSR Omics Radar"
SITE_SUBTITLE = "Scanning the frontiers of bioinformatics, AI, and cancer research."
DEFAULT_BASE_URL = "https://uccc-bbsr.github.io/omics-radar/"

STYLES = """\
:root {
  color-scheme: light;
  --ink: #17252a;
  --muted: #5d6c70;
  --paper: #fbfcfa;
  --card: #ffffff;
  --line: #dce4e1;
  --accent: #006b68;
  --accent-soft: #dcefed;
  --warm: #c95c35;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  background: var(--paper);
  color: var(--ink);
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  line-height: 1.65;
}
a { color: var(--accent); }
.shell { width: min(920px, calc(100% - 2rem)); margin: 0 auto; }
.site-header { padding: 4.5rem 0 2.5rem; border-bottom: 1px solid var(--line); }
.eyebrow { color: var(--warm); font-size: .78rem; font-weight: 800; letter-spacing: .13em; text-transform: uppercase; }
h1 { font-family: Georgia, "Times New Roman", serif; font-size: clamp(2.7rem, 8vw, 5.2rem); line-height: .98; margin: .4rem 0 1rem; letter-spacing: -.045em; }
.subtitle { max-width: 650px; color: var(--muted); font-size: 1.15rem; }
nav { display: flex; gap: 1.25rem; padding-top: 1.25rem; }
nav a { font-weight: 700; text-decoration: none; }
main { padding: 2.5rem 0 5rem; }
.issue-heading { display: flex; justify-content: space-between; gap: 1rem; align-items: end; margin-bottom: 2.5rem; }
.issue-heading h2 { margin: 0; font-family: Georgia, "Times New Roman", serif; font-size: 2rem; }
.date-window { color: var(--muted); white-space: nowrap; }
.category { margin: 3rem 0 1.25rem; padding-bottom: .55rem; border-bottom: 3px solid var(--accent); font-size: 1.35rem; }
.article { padding: 1.5rem 0; border-bottom: 1px solid var(--line); }
.article h3 { margin: 0 0 .55rem; font-family: Georgia, "Times New Roman", serif; font-size: 1.5rem; line-height: 1.25; }
.article h3 a { color: var(--ink); text-decoration-thickness: 1px; text-underline-offset: 4px; }
.article p { margin: .4rem 0; }
.tags { color: var(--muted); font-size: .88rem; }
.tag { display: inline-block; margin: .3rem .25rem 0 0; padding: .14rem .48rem; border-radius: 999px; background: #edf1ef; }
.archive-list { list-style: none; padding: 0; }
.archive-list li { display: flex; justify-content: space-between; gap: 1rem; padding: 1rem 0; border-bottom: 1px solid var(--line); }
.archive-list a { font-weight: 750; }
.empty { padding: 2rem; border: 1px dashed var(--line); border-radius: 10px; color: var(--muted); }
footer { padding: 2rem 0 3rem; border-top: 1px solid var(--line); color: var(--muted); font-size: .9rem; }
@media (max-width: 620px) {
  .site-header { padding-top: 3rem; }
  .issue-heading, .archive-list li { display: block; }
  .date-window { margin-top: .4rem; }
}
"""


def _date_label(value: date) -> str:
    return f"{value.strftime('%B')} {value.day}, {value.year}"


def _page(*, title: str, body: str, asset_prefix: str = "", canonical_url: str = "") -> str:
    canonical = f'<link rel="canonical" href="{escape(canonical_url, quote=True)}">' if canonical_url else ""
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{escape(SITE_SUBTITLE, quote=True)}">
  <title>{escape(title)} · {SITE_TITLE}</title>
  {canonical}
  <link rel="alternate" type="application/rss+xml" title="{SITE_TITLE}" href="{asset_prefix}feed.xml">
  <link rel="stylesheet" href="{asset_prefix}assets/styles.css">
</head>
<body>
  <header class="site-header"><div class="shell">
    <div class="eyebrow">University of Colorado Cancer Center</div>
    <h1>{SITE_TITLE}</h1>
    <p class="subtitle">{SITE_SUBTITLE}</p>
    <nav aria-label="Primary"><a href="{asset_prefix}index.html">Latest issue</a><a href="{asset_prefix}archive.html">Archive</a><a href="{asset_prefix}feed.xml">RSS</a></nav>
  </div></header>
  <main class="shell">{body}</main>
  <footer><div class="shell">Published by the Biostatistics and Bioinformatics Shared Resource.</div></footer>
</body>
</html>
"""


def _article_html(article: dict[str, Any]) -> str:
    tags = "".join(f'<span class="tag">{escape(tag)}</span>' for tag in article.get("tags", []))
    return f"""
<article class="article">
  <h3><a href="{escape(article['url'], quote=True)}" rel="noopener noreferrer">{escape(article['title'])}</a></h3>
  <p>{escape(article['summary'])}</p>
  <div class="tags" aria-label="Tags">{tags}</div>
</article>"""


def render_issue_body(report: dict[str, Any], entries: Iterable[dict[str, Any]]) -> str:
    sections: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for entry in entries:
        sections[entry.get("primary_category") or "Other"].append(entry)
    content = [
        '<section class="issue-heading">',
        f"<div><div class=\"eyebrow\">Monthly briefing</div><h2>{escape(report['title'])}</h2></div>",
        f"<div class=\"date-window\">{_date_label(report['period_start'])}–{_date_label(report['period_end'])}</div>",
        "</section>",
    ]
    if not sections:
        content.append('<p class="empty">No entries were selected for this issue.</p>')
    for category, articles in sections.items():
        content.append(f'<section><h2 class="category">{escape(category)}</h2>')
        content.extend(_article_html(article) for article in articles)
        content.append("</section>")
    return "\n".join(content)


def render_preview(
    *, title: str, period_start: date, period_end: date, entries: Iterable[dict[str, Any]]
) -> str:
    report = {"title": title, "period_start": period_start, "period_end": period_end}
    styles = STYLES.replace("</style>", "")
    return _page(title=title, body=render_issue_body(report, entries)).replace(
        '<link rel="stylesheet" href="assets/styles.css">', f"<style>{styles}</style>"
    )


def build_site(
    database_path: str | Path,
    output_directory: str | Path,
    *,
    base_url: str = DEFAULT_BASE_URL,
) -> list[Path]:
    output = Path(output_directory)
    reports_dir = output / "reports"
    assets_dir = output / "assets"
    reports_dir.mkdir(parents=True, exist_ok=True)
    assets_dir.mkdir(parents=True, exist_ok=True)
    base_url = base_url.rstrip("/") + "/"
    written: list[Path] = []

    stylesheet = assets_dir / "styles.css"
    stylesheet.write_text(STYLES, encoding="utf-8")
    written.append(stylesheet)

    reports = list_published_reports(database_path)
    for report in reports:
        issue_path = reports_dir / f"{report['slug']}.html"
        issue_url = urljoin(base_url, f"reports/{report['slug']}.html")
        issue_path.write_text(
            _page(
                title=report["title"],
                body=render_issue_body(report, get_report_entries(database_path, report["id"])),
                asset_prefix="../",
                canonical_url=issue_url,
            ),
            encoding="utf-8",
        )
        written.append(issue_path)

    if reports:
        latest = reports[0]
        homepage_body = render_issue_body(latest, get_report_entries(database_path, latest["id"]))
    else:
        homepage_body = '<p class="empty">The first issue is being prepared. Please check back soon.</p>'
    index_path = output / "index.html"
    index_path.write_text(
        _page(title="Latest issue", body=homepage_body, canonical_url=base_url), encoding="utf-8"
    )
    written.append(index_path)

    archive_items = "\n".join(
        f'<li><a href="reports/{escape(report["slug"], quote=True)}.html">{escape(report["title"])}</a>'
        f'<span>{_date_label(report["period_start"])}–{_date_label(report["period_end"])}</span></li>'
        for report in reports
    )
    archive_body = "<h2>Issue archive</h2>" + (
        f'<ol class="archive-list">{archive_items}</ol>' if reports else '<p class="empty">No issues have been published yet.</p>'
    )
    archive_path = output / "archive.html"
    archive_path.write_text(
        _page(title="Archive", body=archive_body, canonical_url=urljoin(base_url, "archive.html")),
        encoding="utf-8",
    )
    written.append(archive_path)

    rss = ElementTree.Element("rss", version="2.0")
    channel = ElementTree.SubElement(rss, "channel")
    for tag, value in (
        ("title", SITE_TITLE),
        ("link", base_url),
        ("description", SITE_SUBTITLE),
        ("language", "en-us"),
    ):
        ElementTree.SubElement(channel, tag).text = value
    for report in reports:
        item = ElementTree.SubElement(channel, "item")
        issue_url = urljoin(base_url, f"reports/{report['slug']}.html")
        ElementTree.SubElement(item, "title").text = report["title"]
        ElementTree.SubElement(item, "link").text = issue_url
        ElementTree.SubElement(item, "guid").text = issue_url
        ElementTree.SubElement(item, "description").text = (
            f"BBSR Omics Radar for {_date_label(report['period_start'])} through {_date_label(report['period_end'])}."
        )
        if report.get("published_at"):
            ElementTree.SubElement(item, "pubDate").text = format_datetime(report["published_at"])
    rss_path = output / "feed.xml"
    ElementTree.ElementTree(rss).write(rss_path, encoding="utf-8", xml_declaration=True)
    written.append(rss_path)

    nojekyll = output / ".nojekyll"
    nojekyll.touch()
    written.append(nojekyll)
    return written
