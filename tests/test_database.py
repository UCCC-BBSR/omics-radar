from datetime import date

import duckdb
import pytest

from omics_radar.database import (
    PRIMARY_CATEGORIES,
    create_article,
    get_article,
    initialize_database,
    list_articles,
    update_article,
    validate_url,
)


def test_primary_category_order():
    assert PRIMARY_CATEGORIES[0] == "Software & Tools"
    assert "Security" in PRIMARY_CATEGORIES


def test_entry_crud_and_filters(tmp_path):
    database = tmp_path / "radar.duckdb"
    initialize_database(database)
    article_id = create_article(
        database,
        title="A useful paper",
        summary="A concise editorial summary.",
        date_added=date(2026, 7, 10),
        url="https://example.org/paper",
        primary_category="Software & Tools",
        tags="single-cell, methods, single-cell",
    )

    article = get_article(database, article_id)
    assert article is not None
    assert article["tags"] == ["methods", "single-cell"]
    assert article["primary_category"] == "Software & Tools"
    assert len(
        list_articles(
            database,
            start_date=date(2026, 7, 1),
            end_date=date(2026, 7, 31),
        )
    ) == 1

    update_article(database, article_id, title="An updated title")
    assert get_article(database, article_id)["title"] == "An updated title"


@pytest.mark.parametrize("url", ["example.org", "javascript:alert(1)", "", "ftp://example.org"])
def test_url_validation_rejects_non_web_urls(url):
    with pytest.raises(ValueError):
        validate_url(url)


def test_version_one_database_is_migrated(tmp_path):
    database = tmp_path / "legacy.duckdb"
    with duckdb.connect(str(database)) as connection:
        connection.execute(
            """
            CREATE TABLE articles (
                id VARCHAR, title VARCHAR, summary VARCHAR,
                publication_date DATE, date_added DATE, url VARCHAR,
                source VARCHAR, primary_category VARCHAR, tags VARCHAR,
                status VARCHAR, featured BOOLEAN,
                created_at TIMESTAMPTZ, updated_at TIMESTAMPTZ
            );
            CREATE TABLE reports (
                id VARCHAR, slug VARCHAR, title VARCHAR, period_start DATE,
                period_end DATE, status VARCHAR, published_at TIMESTAMPTZ,
                created_at TIMESTAMPTZ, updated_at TIMESTAMPTZ
            );
            CREATE TABLE report_entries (
                report_id VARCHAR, article_id VARCHAR, sort_order INTEGER,
                title VARCHAR, summary VARCHAR, publication_date DATE,
                url VARCHAR, source VARCHAR, primary_category VARCHAR,
                tags VARCHAR, featured BOOLEAN
            );
            INSERT INTO articles VALUES (
                'entry-1', 'Legacy entry', 'Preserve me', DATE '2026-07-04',
                DATE '2026-07-31', 'https://example.org/legacy', 'Old source',
                'Uncategorized', '["legacy"]', 'draft', TRUE,
                now(), now()
            );
            """
        )

    initialize_database(database)
    entry = get_article(database, "entry-1")
    assert entry is not None
    assert entry["date_added"] == date(2026, 7, 4)
    assert entry["primary_category"] == "Other"
    assert "source" not in entry
    assert "status" not in entry
    assert "featured" not in entry
