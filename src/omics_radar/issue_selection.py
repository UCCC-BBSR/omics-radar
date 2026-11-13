"""Readable, filterable entry selection for the issue editor."""

from __future__ import annotations

from typing import Any
from pathlib import Path

import streamlit as st

from omics_radar.database import update_article


def select_issue_entries(
    candidates: list[dict[str, Any]], *, scope: str, database_path: str | Path | None = None
) -> list[str]:
    prefix = f"issue_entries_{scope}"
    state_key = f"{prefix}_selection"
    selection = st.session_state.setdefault(state_key, {})
    for article in candidates:
        selection.setdefault(article["id"], True)

    st.markdown("### Entries in this issue")
    if message := st.session_state.pop(f"{prefix}_saved", None):
        st.success(message)
    if not candidates:
        st.info("No entries match this issue's date range.")
        return []

    search_col, category_col = st.columns([2, 1])
    query = search_col.text_input(
        "Find entries", placeholder="Search titles, summaries or tags", key=f"{prefix}_search"
    ).strip().casefold()
    category = category_col.selectbox(
        "Filter by category",
        ["All categories", *sorted({a["primary_category"] for a in candidates})],
        key=f"{prefix}_category",
    )
    visible = [
        article for article in candidates
        if (category == "All categories" or article["primary_category"] == category)
        and query in " ".join([
            article["title"], article["summary"], article["primary_category"], *article["tags"]
        ]).casefold()
    ]

    def set_visible(included: bool) -> None:
        for article in visible:
            article_id = article["id"]
            st.session_state[state_key][article_id] = included
            st.session_state[f"{prefix}_include_{article_id}"] = included

    def save_choice(article_id: str) -> None:
        st.session_state[state_key][article_id] = st.session_state[f"{prefix}_include_{article_id}"]

    include_col, exclude_col = st.columns(2)
    include_col.button(
        "Include all shown", key=f"{prefix}_include_shown",
        on_click=set_visible, args=(True,), disabled=not visible,
    )
    exclude_col.button(
        "Exclude all shown", key=f"{prefix}_exclude_shown",
        on_click=set_visible, args=(False,), disabled=not visible,
    )
    selected_ids = [a["id"] for a in candidates if selection[a["id"]]]
    st.caption(
        f"{len(selected_ids)} of {len(candidates)} entries included · {len(visible)} shown. "
        "Filters only change what you see; hidden entries keep their inclusion settings."
    )
    if not visible:
        st.info("No entries match these filters. Clear the search or change the category.")
    else:
        with st.container(height=600, border=True):
            for article in visible:
                article_id = article["id"]
                widget_key = f"{prefix}_include_{article_id}"
                # Keep selection outside widget state: Streamlit removes widgets
                # hidden by a filter, but their inclusion choices must survive.
                st.session_state[widget_key] = selection[article_id]
                with st.container(border=True):
                    st.checkbox(
                        "Include in issue", key=widget_key,
                        on_change=save_choice, args=(article_id,),
                    )
                    st.write(article["title"])
                    st.caption(f"{article['primary_category']} · Added {article['date_added']}")
                    st.write(article["summary"])
                    if article["tags"]:
                        st.caption("Tags: " + ", ".join(article["tags"]))
                    st.link_button("Read source", article["url"])
                    if database_path is not None:
                        with st.expander("Edit entry"):
                            st.caption("Save changes before previewing or publishing. Changes update the database entry.")
                            # Refresh form defaults when another editor saves this entry.
                            form_key = f"{prefix}_edit_{article_id}_{article.get('updated_at', '')}"
                            with st.form(form_key):
                                title = st.text_input("Title", value=article["title"], key=f"{form_key}_title")
                                summary = st.text_area(
                                    "Summary", value=article["summary"], height=150, key=f"{form_key}_summary"
                                )
                                tags = st.text_input(
                                    "Tags", value=", ".join(article["tags"]),
                                    help="Separate tags with commas.", key=f"{form_key}_tags"
                                )
                                saved = st.form_submit_button("Save entry changes")
                            if saved:
                                try:
                                    update_article(
                                        database_path, article_id, title=title, summary=summary, tags=tags
                                    )
                                except Exception as error:
                                    st.error(str(error))
                                else:
                                    st.session_state[f"{prefix}_saved"] = f"Saved changes to {title.strip()}."
                                    st.rerun()
    return selected_ids
