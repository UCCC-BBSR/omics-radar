from __future__ import annotations

import calendar
import sys
from datetime import date
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from omics_radar.database import (  # noqa: E402
    ARTICLE_STATUSES,
    create_article,
    delete_article,
    get_article,
    initialize_database,
    list_articles,
    save_published_report,
    update_article,
)
from omics_radar.publishing import DEFAULT_BASE_URL, build_site, render_preview  # noqa: E402


DATABASE_PATH = ROOT / "data" / "omics_radar.duckdb"
DOCS_PATH = ROOT / "docs"


def month_window(today: date) -> tuple[date, date]:
    return today.replace(day=1), today.replace(day=calendar.monthrange(today.year, today.month)[1])


def show_error(error: Exception) -> None:
    message = str(error)
    if "Duplicate key" in message and "url" in message.lower():
        message = "An article with this URL already exists."
    st.error(message)


st.set_page_config(page_title="BBSR Omics Radar Editor", page_icon="📡", layout="wide")
initialize_database(DATABASE_PATH)

st.title("BBSR Omics Radar")
st.caption("Local editorial workspace · changes remain local until generated files are committed and pushed")

add_tab, manage_tab, publish_tab = st.tabs(["Add article", "Manage articles", "Publish issue"])

with add_tab:
    st.subheader("Add an article")
    with st.form("add_article", clear_on_submit=True):
        title = st.text_input("Title")
        summary = st.text_area("Summary", height=150)
        left, right = st.columns(2)
        publication_date = left.date_input("Publication date", value=date.today())
        url = right.text_input("URL", placeholder="https://…")
        source = left.text_input("Source", placeholder="Journal, lab, or publication")
        category = right.text_input("Primary category", value="Uncategorized")
        tags = st.text_input("Tags", placeholder="bioinformatics, AI, cancer research")
        status = left.selectbox("Status", ARTICLE_STATUSES, index=0)
        featured = right.checkbox("Featured article")
        submitted = st.form_submit_button("Add article", type="primary")
    if submitted:
        try:
            create_article(
                DATABASE_PATH,
                title=title,
                summary=summary,
                publication_date=publication_date,
                url=url,
                source=source,
                primary_category=category,
                tags=tags,
                status=status,
                featured=featured,
            )
            st.success("Article added.")
        except Exception as error:
            show_error(error)

with manage_tab:
    st.subheader("Review and edit")
    default_start, default_end = month_window(date.today())
    filters = st.columns([1, 1, 2])
    filter_start = filters[0].date_input("From", value=default_start, key="manage_start")
    filter_end = filters[1].date_input("Through", value=default_end, key="manage_end")
    filter_statuses = filters[2].multiselect("Statuses", ARTICLE_STATUSES, default=list(ARTICLE_STATUSES))
    articles = list_articles(
        DATABASE_PATH, start_date=filter_start, end_date=filter_end, statuses=filter_statuses
    )
    st.write(f"{len(articles)} article{'s' if len(articles) != 1 else ''}")
    if articles:
        st.dataframe(
            [
                {
                    "Date": article["publication_date"],
                    "Title": article["title"],
                    "Category": article["primary_category"],
                    "Tags": ", ".join(article["tags"]),
                    "Status": article["status"],
                    "Featured": article["featured"],
                }
                for article in articles
            ],
            use_container_width=True,
            hide_index=True,
        )
        labels = {article["id"]: f"{article['publication_date']} · {article['title']}" for article in articles}
        selected_id = st.selectbox("Article to edit", labels, format_func=labels.get)
        selected = get_article(DATABASE_PATH, selected_id)
        if selected:
            with st.form("edit_article"):
                edit_title = st.text_input("Title", value=selected["title"])
                edit_summary = st.text_area("Summary", value=selected["summary"], height=150)
                edit_left, edit_right = st.columns(2)
                edit_date = edit_left.date_input("Publication date", value=selected["publication_date"])
                edit_url = edit_right.text_input("URL", value=selected["url"])
                edit_source = edit_left.text_input("Source", value=selected["source"])
                edit_category = edit_right.text_input("Primary category", value=selected["primary_category"])
                edit_tags = st.text_input("Tags", value=", ".join(selected["tags"]))
                edit_status = edit_left.selectbox(
                    "Status", ARTICLE_STATUSES, index=ARTICLE_STATUSES.index(selected["status"])
                )
                edit_featured = edit_right.checkbox("Featured article", value=selected["featured"])
                saved = st.form_submit_button("Save changes", type="primary")
            if saved:
                try:
                    update_article(
                        DATABASE_PATH,
                        selected_id,
                        title=edit_title,
                        summary=edit_summary,
                        publication_date=edit_date,
                        url=edit_url,
                        source=edit_source,
                        primary_category=edit_category,
                        tags=edit_tags,
                        status=edit_status,
                        featured=edit_featured,
                    )
                    st.success("Article updated.")
                    st.rerun()
                except Exception as error:
                    show_error(error)
            with st.expander("Delete this article"):
                confirm_delete = st.checkbox("I understand this cannot be undone", key=f"confirm_{selected_id}")
                if st.button("Delete article", disabled=not confirm_delete, type="secondary"):
                    delete_article(DATABASE_PATH, selected_id)
                    st.success("Article deleted.")
                    st.rerun()
    else:
        st.info("No articles match this date range and status filter.")

with publish_tab:
    st.subheader("Preview and publish an issue")
    default_start, default_end = month_window(date.today())
    publish_left, publish_right = st.columns(2)
    issue_start = publish_left.date_input("Issue starts", value=default_start)
    issue_end = publish_right.date_input("Issue ends", value=default_end)
    issue_slug = publish_left.text_input("Issue slug", value=issue_start.strftime("%Y-%m"))
    issue_title = publish_right.text_input("Issue title", value=issue_start.strftime("%B %Y"))
    base_url = st.text_input("Public site URL", value=DEFAULT_BASE_URL)
    candidates = list_articles(
        DATABASE_PATH, start_date=issue_start, end_date=issue_end, statuses=("ready", "published")
    )
    candidate_labels = {
        article["id"]: f"{article['primary_category']} · {article['title']}" for article in candidates
    }
    selected_ids = st.multiselect(
        "Articles in this issue",
        candidate_labels,
        default=list(candidate_labels),
        format_func=candidate_labels.get,
    )
    selected_articles = [article for article in candidates if article["id"] in selected_ids]
    preview_col, publish_col = st.columns(2)
    if preview_col.button("Preview selected issue", use_container_width=True):
        if selected_articles:
            components.html(
                render_preview(
                    title=issue_title,
                    period_start=issue_start,
                    period_end=issue_end,
                    entries=selected_articles,
                ),
                height=800,
                scrolling=True,
            )
        else:
            st.warning("Select at least one article to preview.")
    if publish_col.button("Publish static issue", type="primary", use_container_width=True):
        try:
            if issue_start > issue_end:
                raise ValueError("The issue start date must be on or before its end date.")
            if not issue_slug or any(character not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_" for character in issue_slug):
                raise ValueError("The issue slug may contain only letters, numbers, hyphens, and underscores.")
            save_published_report(
                DATABASE_PATH,
                slug=issue_slug,
                title=issue_title,
                period_start=issue_start,
                period_end=issue_end,
                article_ids=selected_ids,
            )
            generated = build_site(DATABASE_PATH, DOCS_PATH, base_url=base_url)
            st.success(f"Published {issue_slug} and generated {len(generated)} files in docs/.")
            st.code(f"docs/reports/{issue_slug}.html")
        except Exception as error:
            show_error(error)
