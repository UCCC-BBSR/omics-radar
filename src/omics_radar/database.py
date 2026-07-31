from __future__ import annotations

import json
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlparse
from uuid import uuid4

import duckdb


ARTICLE_STATUSES = ("draft", "ready", "published")


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _connect(database_path: str | Path) -> duckdb.DuckDBPyConnection:
    path = Path(database_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    return duckdb.connect(str(path))


def initialize_database(database_path: str | Path) -> None:
    with _connect(database_path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS articles (
                id VARCHAR PRIMARY KEY,
                title VARCHAR NOT NULL,
                summary VARCHAR NOT NULL,
                publication_date DATE NOT NULL,
                date_added DATE NOT NULL,
                url VARCHAR NOT NULL UNIQUE,
                source VARCHAR NOT NULL,
                primary_category VARCHAR NOT NULL,
                tags VARCHAR NOT NULL,
                status VARCHAR NOT NULL,
                featured BOOLEAN NOT NULL DEFAULT FALSE,
                created_at TIMESTAMPTZ NOT NULL,
                updated_at TIMESTAMPTZ NOT NULL,
                CHECK (status IN ('draft', 'ready', 'published'))
            );

            CREATE TABLE IF NOT EXISTS reports (
                id VARCHAR PRIMARY KEY,
                slug VARCHAR NOT NULL UNIQUE,
                title VARCHAR NOT NULL,
                period_start DATE NOT NULL,
                period_end DATE NOT NULL,
                status VARCHAR NOT NULL,
                published_at TIMESTAMPTZ,
                created_at TIMESTAMPTZ NOT NULL,
                updated_at TIMESTAMPTZ NOT NULL,
                CHECK (status IN ('draft', 'published'))
            );

            CREATE TABLE IF NOT EXISTS report_entries (
                report_id VARCHAR NOT NULL,
                article_id VARCHAR NOT NULL,
                sort_order INTEGER NOT NULL,
                title VARCHAR NOT NULL,
                summary VARCHAR NOT NULL,
                publication_date DATE NOT NULL,
                url VARCHAR NOT NULL,
                source VARCHAR NOT NULL,
                primary_category VARCHAR NOT NULL,
                tags VARCHAR NOT NULL,
                featured BOOLEAN NOT NULL,
                PRIMARY KEY (report_id, article_id)
            );
            """
        )


def _rows(connection: duckdb.DuckDBPyConnection) -> list[dict[str, Any]]:
    columns = [item[0] for item in connection.description]
    return [dict(zip(columns, row, strict=True)) for row in connection.fetchall()]


def normalize_tags(tags: str | Iterable[str]) -> list[str]:
    values = tags.split(",") if isinstance(tags, str) else tags
    return sorted({value.strip() for value in values if value and value.strip()}, key=str.casefold)


def decode_tags(value: str | None) -> list[str]:
    if not value:
        return []
    try:
        decoded = json.loads(value)
    except json.JSONDecodeError:
        return normalize_tags(value)
    return normalize_tags(decoded if isinstance(decoded, list) else [])


def validate_url(url: str) -> str:
    cleaned = url.strip()
    parsed = urlparse(cleaned)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("URL must be a complete http:// or https:// address.")
    return cleaned


def create_article(
    database_path: str | Path,
    *,
    title: str,
    summary: str,
    publication_date: date,
    url: str,
    source: str = "",
    primary_category: str = "Uncategorized",
    tags: str | Iterable[str] = (),
    status: str = "draft",
    featured: bool = False,
) -> str:
    if status not in ARTICLE_STATUSES:
        raise ValueError(f"Unknown article status: {status}")
    if not title.strip() or not summary.strip():
        raise ValueError("Title and summary are required.")
    article_id = str(uuid4())
    timestamp = _now()
    with _connect(database_path) as connection:
        connection.execute(
            """
            INSERT INTO articles VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                article_id,
                title.strip(),
                summary.strip(),
                publication_date,
                date.today(),
                validate_url(url),
                source.strip(),
                primary_category.strip() or "Uncategorized",
                json.dumps(normalize_tags(tags)),
                status,
                featured,
                timestamp,
                timestamp,
            ],
        )
    return article_id


def update_article(database_path: str | Path, article_id: str, **values: Any) -> None:
    allowed = {
        "title",
        "summary",
        "publication_date",
        "url",
        "source",
        "primary_category",
        "tags",
        "status",
        "featured",
    }
    unknown = set(values) - allowed
    if unknown:
        raise ValueError(f"Unknown article fields: {', '.join(sorted(unknown))}")
    if "status" in values and values["status"] not in ARTICLE_STATUSES:
        raise ValueError(f"Unknown article status: {values['status']}")
    if "url" in values:
        values["url"] = validate_url(values["url"])
    if "tags" in values:
        values["tags"] = json.dumps(normalize_tags(values["tags"]))
    for required in ("title", "summary"):
        if required in values and not str(values[required]).strip():
            raise ValueError(f"{required.title()} is required.")
    if "primary_category" in values:
        values["primary_category"] = str(values["primary_category"]).strip() or "Uncategorized"
    for field in ("title", "summary", "source"):
        if field in values:
            values[field] = str(values[field]).strip()
    values["updated_at"] = _now()
    assignments = ", ".join(f"{name} = ?" for name in values)
    parameters = [*values.values(), article_id]
    with _connect(database_path) as connection:
        result = connection.execute(
            f"UPDATE articles SET {assignments} WHERE id = ? RETURNING id", parameters
        ).fetchone()
    if result is None:
        raise KeyError(f"Article not found: {article_id}")


def delete_article(database_path: str | Path, article_id: str) -> None:
    with _connect(database_path) as connection:
        connection.execute("DELETE FROM articles WHERE id = ?", [article_id])


def get_article(database_path: str | Path, article_id: str) -> dict[str, Any] | None:
    with _connect(database_path) as connection:
        result = connection.execute("SELECT * FROM articles WHERE id = ?", [article_id])
        rows = _rows(result)
    if not rows:
        return None
    rows[0]["tags"] = decode_tags(rows[0]["tags"])
    return rows[0]


def list_articles(
    database_path: str | Path,
    *,
    start_date: date | None = None,
    end_date: date | None = None,
    statuses: Iterable[str] | None = None,
) -> list[dict[str, Any]]:
    clauses: list[str] = []
    parameters: list[Any] = []
    if start_date:
        clauses.append("publication_date >= ?")
        parameters.append(start_date)
    if end_date:
        clauses.append("publication_date <= ?")
        parameters.append(end_date)
    if statuses:
        selected = list(statuses)
        clauses.append(f"status IN ({', '.join('?' for _ in selected)})")
        parameters.extend(selected)
    where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    with _connect(database_path) as connection:
        result = connection.execute(
            f"""
            SELECT * FROM articles {where}
            ORDER BY featured DESC, publication_date DESC, title
            """,
            parameters,
        )
        rows = _rows(result)
    for row in rows:
        row["tags"] = decode_tags(row["tags"])
    return rows


def save_published_report(
    database_path: str | Path,
    *,
    slug: str,
    title: str,
    period_start: date,
    period_end: date,
    article_ids: list[str],
) -> str:
    if not article_ids:
        raise ValueError("Select at least one article before publishing.")
    timestamp = _now()
    with _connect(database_path) as connection:
        existing = connection.execute("SELECT id FROM reports WHERE slug = ?", [slug]).fetchone()
        report_id = existing[0] if existing else str(uuid4())
        connection.begin()
        try:
            if existing:
                connection.execute(
                    """
                    UPDATE reports SET title = ?, period_start = ?, period_end = ?,
                        status = 'published', published_at = ?, updated_at = ?
                    WHERE id = ?
                    """,
                    [title.strip(), period_start, period_end, timestamp, timestamp, report_id],
                )
                connection.execute("DELETE FROM report_entries WHERE report_id = ?", [report_id])
            else:
                connection.execute(
                    "INSERT INTO reports VALUES (?, ?, ?, ?, ?, 'published', ?, ?, ?)",
                    [report_id, slug, title.strip(), period_start, period_end, timestamp, timestamp, timestamp],
                )
            for sort_order, article_id in enumerate(article_ids):
                article = connection.execute(
                    """
                    SELECT id, title, summary, publication_date, url, source,
                           primary_category, tags, featured
                    FROM articles WHERE id = ?
                    """,
                    [article_id],
                ).fetchone()
                if article is None:
                    raise KeyError(f"Article not found: {article_id}")
                connection.execute(
                    "INSERT INTO report_entries VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    [report_id, article[0], sort_order, *article[1:]],
                )
            connection.execute(
                f"UPDATE articles SET status = 'published', updated_at = ? WHERE id IN ({', '.join('?' for _ in article_ids)})",
                [timestamp, *article_ids],
            )
            connection.commit()
        except Exception:
            connection.rollback()
            raise
    return report_id


def list_published_reports(database_path: str | Path) -> list[dict[str, Any]]:
    with _connect(database_path) as connection:
        result = connection.execute(
            """
            SELECT * FROM reports WHERE status = 'published'
            ORDER BY period_end DESC, published_at DESC
            """
        )
        return _rows(result)


def get_report_entries(database_path: str | Path, report_id: str) -> list[dict[str, Any]]:
    with _connect(database_path) as connection:
        result = connection.execute(
            "SELECT * FROM report_entries WHERE report_id = ? ORDER BY sort_order",
            [report_id],
        )
        rows = _rows(result)
    for row in rows:
        row["tags"] = decode_tags(row["tags"])
    return rows
