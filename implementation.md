# BBSR Omics Radar implementation plan

## Objective

Build a local editorial application for collecting and reviewing entries, then
publish a static monthly newsletter for the `UCCC-BBSR/omics-radar` GitHub
repository.

The public site title is **BBSR Omics Radar** and its subtitle is **Scanning the
frontiers of bioinformatics, AI, and cancer research.**

## Architecture

```text
Local Streamlit admin app
        |
        +-- Add, edit, and delete entries
        +-- Filter and review entries in DuckDB
        +-- Select entries and preview an issue
        +-- Publish static output
                    |
                    v
                  docs/
        +-- index.html          (latest issue)
        +-- archive.html        (all issues)
        +-- feed.xml            (RSS feed)
        +-- reports/YYYY-MM.html
        +-- assets/styles.css
                    |
                    v
                GitHub Pages
```

Streamlit and DuckDB run locally. GitHub Pages hosts only the generated static
files; it cannot run Streamlit or provide database writes.

## Repository structure

```text
omics-radar/
├── app.py
├── src/omics_radar/
│   ├── database.py
│   └── publishing.py
├── data/
│   └── omics_radar.duckdb      # created locally on first run
├── docs/
│   ├── index.html
│   ├── archive.html
│   ├── feed.xml
│   ├── reports/
│   └── assets/
├── tests/
├── idea.md
├── implementation.md
└── pyproject.toml
```

## Data model

### `articles`

- `id`: UUID string
- `title`
- `summary`
- `date_added`
- `url`
- `primary_category`
- `tags`: JSON array stored as text
- `created_at`
- `updated_at`

`primary_category` determines the newsletter section. Tags are secondary labels
used for discovery and filtering. This prevents multi-tag entries from being
duplicated across newsletter sections.

The category dropdown initially contains:

- Software & Tools
- Cancer Research
- AI & Machine Learning
- Technology Platforms
- Security
- Community
- Other

The choices live in one shared constant so categories can be added later without
changing the database schema.

### `reports`

- `id`: UUID string
- `slug`: normally `YYYY-MM`
- `title`
- `period_start`
- `period_end`
- `published_at`
- `created_at`
- `updated_at`

### `report_entries`

This table records the selected entry IDs and a snapshot of their publishable
fields. Snapshots ensure a published issue does not silently change when the
working entry is edited later.

## Editorial workflow

1. Clone or pull `UCCC-BBSR/omics-radar`.
2. Run `uv sync`.
3. Start the editor with `uv run streamlit run app.py`.
4. Add imported or manually curated entries.
5. Review and categorize entries.
6. Choose a reporting window; all entries in that window are available for selection.
7. Preview the issue.
8. Publish the issue.
9. The application regenerates the latest-issue homepage, archive, issue pages,
   stylesheet, and RSS feed.
10. Review the generated files, commit, and push them.
11. GitHub Pages deploys the contents of `docs/`.

## Publishing approach

The implementation generates HTML locally and commits `docs/` to the default
branch. The included GitHub Actions workflow deploys that directory as a Pages
artifact whenever published files reach `main`. The repository's Pages source
must be set to **GitHub Actions** once by a repository administrator.

The default site URL is:

`https://uccc-bbsr.github.io/omics-radar/`

The DuckDB file is ignored by default so drafts and editorial metadata are not
accidentally exposed in a public repository. If the team wants the database to
be shared through Git, that can be changed deliberately after reviewing its
contents and repository visibility.

## Milestones

1. **MVP:** database schema, entry CRUD, date filtering, issue selection,
   preview, static publishing, archive, and RSS.
2. **Editorial improvements:** bulk import, duplicate URL detection, richer
   search, validation, and configurable category ordering.
3. **Publishing improvements:** custom domain, analytics, accessibility audit,
   and automated link checking.
4. **Optional collaboration:** move editorial data to a shared service if more
   than one curator needs simultaneous access.

## Key constraints and decisions

- GitHub Pages is suitable for the public newsletter, not the admin UI.
- Static output contains only published content.
- Re-publishing an existing slug replaces that report after confirmation in the
  local workflow; report-entry snapshots keep publication output stable.
- Publishing files is separate from committing and pushing them. The app will
  not perform Git operations without an explicit user action.
