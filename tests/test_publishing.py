from datetime import date

from omics_radar.database import (
    create_article,
    get_report_entries,
    initialize_database,
    save_published_report,
    update_article,
)
from omics_radar.publishing import build_site


def test_publish_builds_site_and_snapshots_article(tmp_path):
    database = tmp_path / "radar.duckdb"
    output = tmp_path / "docs"
    initialize_database(database)
    article_id = create_article(
        database,
        title="New cancer atlas",
        summary="Researchers present a new atlas.",
        date_added=date(2026, 7, 12),
        url="https://example.org/atlas",
        primary_category="Cancer Research",
        tags=("atlas", "single-cell"),
    )
    report_id = save_published_report(
        database,
        slug="2026-07",
        title="July 2026",
        period_start=date(2026, 7, 1),
        period_end=date(2026, 7, 31),
        article_ids=[article_id],
    )

    update_article(database, article_id, title="Working copy changed")
    assert get_report_entries(database, report_id)[0]["title"] == "New cancer atlas"

    written = build_site(database, output, base_url="https://uccc-bbsr.github.io/omics-radar/")
    assert output / "index.html" in written
    assert (output / "archive.html").exists()
    assert (output / "feed.xml").exists()
    assert (output / ".nojekyll").exists()
    issue = (output / "reports" / "2026-07.html").read_text()
    assert "New cancer atlas" in issue
    assert "Working copy changed" not in issue
    assert "Cancer Research" in issue
    assert "../assets/styles.css" in issue


def test_republishing_slug_replaces_snapshot(tmp_path):
    database = tmp_path / "radar.duckdb"
    initialize_database(database)
    first = create_article(
        database,
        title="First",
        summary="First summary",
        date_added=date(2026, 7, 1),
        url="https://example.org/first",
    )
    second = create_article(
        database,
        title="Second",
        summary="Second summary",
        date_added=date(2026, 7, 2),
        url="https://example.org/second",
    )
    report_id = save_published_report(
        database,
        slug="2026-07",
        title="July",
        period_start=date(2026, 7, 1),
        period_end=date(2026, 7, 31),
        article_ids=[first],
    )
    replaced_id = save_published_report(
        database,
        slug="2026-07",
        title="July revised",
        period_start=date(2026, 7, 1),
        period_end=date(2026, 7, 31),
        article_ids=[second],
    )
    entries = get_report_entries(database, report_id)
    assert replaced_id == report_id
    assert [entry["title"] for entry in entries] == ["Second"]
