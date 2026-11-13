# BBSR Omics Radar

A local Streamlit editorial application and static newsletter publisher for the
University of Colorado Cancer Center Biostatistics and Bioinformatics Shared
Resource.

[Read the public newsletter](https://uccc-bbsr.github.io/omics-radar/index.html).

## Run locally

Requires Python 3.11 or later and `uv`.

```bash
uv sync
uv run streamlit run app.py
```

Open the local URL printed by Streamlit (normally `http://localhost:8501`). The
app creates its database at `data/omics_radar.duckdb`. This repository tracks the
database in Git; saved editorial changes remain local until committed and pushed.
GitHub Pages hosts the generated newsletter, while editing runs locally.

## Curate a month with Codex

Use [monthly-prompt.md](monthly-prompt.md) as the maintained curation instructions.
For example:

> Follow monthly-prompt.md for November 2026, including the software update
> checks, and add any missing entries with an entry date of November 30, 2026.

Run a full-month request after the month ends. For an ongoing month, specify an
elapsed date range. Add **preview only** to review candidates without writing to
the database, or specify a topic focus or explicit maximum number of entries.

The workflow checks research sources and official software release histories,
verifies dates, deduplicates against entries across all months, backs up the
database, and adds verified entries. Curation does **not** publish an issue,
regenerate the public site, commit, or push.

Important date and coverage rules:

- The research window is based on verified publication, posting, or release dates.
  `date_added` is the assigned editorial date used by the app's issue filters.
- Substantive blog coverage within the month can qualify even when the underlying
  paper is older. Record both dates and avoid duplicating an already covered study.
- Preprints are labeled, and uncertain dates or inaccessible evidence remain
  unresolved rather than being guessed.
- The usual 15–25 entry target does not stop source checks or exclude additional
  verified priority items unless an explicit maximum was requested.
- Save source coverage, evidence, exclusions, and unresolved candidates in the
  curation audit. Existing audits are in `data/curation-YYYY-MM*.json` and `.html`;
  database backups are in `data/backups/`. Publication dates and supporting
  evidence belong in these audits because the database has no publication-date field.

## Research and discovery sources

### Core monthly coverage

- [RNA-seq Blog](https://www.rna-seqblog.com/) — transcriptomics methods and news.
- [bioRxiv](https://www.biorxiv.org/) — bioinformatics, genomics, cancer biology,
  and systems biology preprints; use the [official metadata API](https://api.biorxiv.org/).
- [Nature Methods](https://www.nature.com/nmeth/articles) — computational methods,
  single-cell and spatial omics, benchmarks, and research software.
- [Nature Biotechnology](https://www.nature.com/nbt/articles) — biotechnology,
  multiomics, cancer technologies, and analysis methods.
- [Other Nature journals](https://www.nature.com/) — especially Nature Genetics,
  Nature Cancer, and Nature Communications.
- [Science journals](https://www.science.org/) — Science, Science Advances, and
  Science Translational Medicine.
- [Python Weekly](https://www.pythonweekly.com/archive/) and
  [Planet Python](https://planetpython.org/) — Python tools and practical tutorials.
- [R-bloggers](https://www.r-bloggers.com/) — statistics, visualization, and R packages.
- [Posit Open Source Blog](https://opensource.posit.co/blog/) — R/Python tooling
  and reproducible research.

### Focused sources

- [Bioconductor community blog](https://blog.bioconductor.org/)
- [scverse blog](https://scverse.org/blog/)
- [nf-core blog](https://nf-co.re/blog)
- [Ming Tang's blog](https://divingintogeneticsandgenomics.com/)
- [Genome Biology](https://link.springer.com/journal/13059)
- [BMC Bioinformatics](https://link.springer.com/journal/12859)
- [Bioinformatics (Oxford University Press)](https://academic.oup.com/bioinformatics)
- [PLOS Computational Biology](https://journals.plos.org/ploscompbiol/)
- [Bioinformatics Blogs Aggregator](https://bioinf-bloggers.com)
- [PyCoder's Weekly](https://pycoders.com/)
- [Python Bytes Podcast](https://pythonbytes.fm/)

Aggregators and newsletters aid discovery; verify linked developments against
original posts, papers, and official project sources.

### Preventing coverage gaps

The [required first-pass procedures](monthly-prompt.md#required-first-pass-research-coverage)
incorporate lessons from the September and October curation runs:

- **RNA-seq Blog:** query its public WordPress API alongside dated archives,
  follow pagination, reconcile returned totals, and screen every in-window title.
  A homepage or stale tag page is insufficient.
- **Nature Methods and Nature Biotechnology:** enumerate each journal separately
  using paginated, all-content listings. Include relevant Analyses, Resources,
  Brief Communications, and other article types; do not limit discovery to titles
  containing “RNA-seq” or “cancer.” Verify first-online dates rather than issue dates.
- **bioRxiv:** enumerate the requested interval and relevant categories through
  the official API, follow every page, and verify version dates and publication lineage.
- **Fallbacks:** try dated archives, public APIs, RSS, publisher metadata/Crossref,
  Europe PMC/PubMed abstracts, and author or project resources as appropriate.
  A current RSS feed may not cover a historical month. Record abstract-only access
  and incomplete coverage; failed retrieval does not mean there were no updates.

## Software and AI update checks

Every monthly run checks **Python, R, uv, renv, Nextflow, RStudio, Positron,
VS Code, ChatGPT, Codex, Claude, and Claude Code**.

Additional research-computing coverage includes **Bioconductor, Quarto, Snakemake,
nf-core pipelines, Scanpy/scverse, Ruff, Polars, and DuckDB**, plus relevant tools
discovered during research. The maintained
[software watchlist](monthly-prompt.md#software-and-ai-product-watchlist) contains
official release URLs and the detailed selection checklist.

Include substantial features, breaking changes, support changes, and consequential
security, numerical-correctness, data-integrity, or reproducibility fixes. Routine
maintenance does not need an entry. Check actual release dates and stable/preview
status; for AI products, distinguish model, API, chat, and coding-agent availability.
Record an outcome for every required product, even if no entry qualifies. These
checks research updates; they do not install or upgrade software.

## Review and publish an issue

1. **Add entry** creates individual records. **Manage entries** supports full
   editing, including category, URL, and entry date, as well as deletion.
2. In **Publish issue**, set the inclusive start/end dates, issue slug (normally
   `YYYY-MM`), title, and public site URL. Candidate entries are filtered by
   `date_added`, not the underlying publication date.
3. Review the scrollable entry cards showing full titles, summaries, categories,
   tags, and source links. Use **Include in issue** to select entries; new candidates
   start included. Search titles, summaries, or tags and filter by category.
4. **Include all shown** and **Exclude all shown** affect only the filtered list.
   Hidden entries retain their selections. Inclusion choices are kept per date
   range within the current session; they are not saved issue drafts and may reset
   after a browser-session or server restart.
5. Expand **Edit entry** on a card to change its title, summary, and comma-separated
   tags. Click **Save entry changes** before previewing or publishing. Saving updates
   the database entry and preserves inclusion choices; title and summary are required.
6. Click **Preview selected issue** to review the output, then **Publish static issue**
   to save a report snapshot and regenerate `docs/`.
7. Review the generated files, then commit and push when ready to make them public.
   The GitHub Actions workflow deploys `docs/` when those files change on `main`.
   Repository Pages settings must use **GitHub Actions** as the source.

Published issues store snapshots: later entry edits do not silently change existing
issues. Publishing with an existing slug replaces that issue's snapshot and selection.
The Publish button generates local files; it does not commit or push them.

Generated output includes `docs/index.html`, `docs/archive.html`, `docs/feed.xml`,
individual issues under `docs/reports/`, and styles under `docs/assets/`.

## Troubleshooting and tests

After code changes, refresh or rerun the Streamlit page. The issue renderer reloads
with the app to avoid retaining an older function signature. If an error persists,
restart your local Streamlit process with the run command above; unsaved form edits
and session-only selections may be lost, while saved database entries remain.

If a curation write encounters a database lock, stop and resolve the active writer
before retrying. Keep a recoverable backup before bulk imports or backfills.

```bash
uv run pytest
```

Tests cover database operations, publishing, issue selection and filtering, inline
editing, validation, and recovery from a stale imported issue renderer.

See [implementation.md](implementation.md) for the architecture and data model;
[monthly-prompt.md](monthly-prompt.md) is the detailed source of truth for curation.
