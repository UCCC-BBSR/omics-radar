from datetime import date

import pytest

from omics_radar.database import (
    create_article,
    get_article,
    initialize_database,
    list_articles,
    update_article,
    validate_url,
)


def test_article_crud_and_filters(tmp_path):
    database = tmp_path / "radar.duckdb"
    initialize_database(database)
    article_id = create_article(
        database,
        title="A useful paper",
        summary="A concise editorial summary.",
        publication_date=date(2026, 7, 10),
        url="https://example.org/paper",
        source="Example Journal",
        primary_category="Bioinformatics",
        tags="single-cell, methods, single-cell",
        status="ready",
        featured=True,
    )

    article = get_article(database, article_id)
    assert article is not None
    assert article["tags"] == ["methods", "single-cell"]
    assert article["featured"] is True
    assert len(
        list_articles(
            database,
            start_date=date(2026, 7, 1),
            end_date=date(2026, 7, 31),
            statuses=("ready",),
        )
    ) == 1

    update_article(database, article_id, title="An updated title", status="published")
    assert get_article(database, article_id)["title"] == "An updated title"
    assert list_articles(database, statuses=("ready",)) == []


@pytest.mark.parametrize("url", ["example.org", "javascript:alert(1)", "", "ftp://example.org"])
def test_url_validation_rejects_non_web_urls(url):
    with pytest.raises(ValueError):
        validate_url(url)
