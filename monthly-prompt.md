# Monthly Omics Radar curation prompt

Use this file later to ask Codex to research and add entries. Creating or editing
this prompt does not itself authorize a curation run.

## Example requests

> Follow `monthly-prompt.md` to add entries for August 2026. Scan articles and
> posts published August 1–31, 2026, inclusive, and set every new entry's
> `date_added` to August 31, 2026.

> Follow `monthly-prompt.md` for September 1–15, 2026, inclusive. Set every new
> entry's `date_added` to September 15, 2026. Focus on single-cell and spatial
> omics methods.

> Follow `monthly-prompt.md` for September 2026, with an entry date of September
> 30, 2026. Check research sources and the software watchlist, including major
> releases, meaningful feature updates, and important security or compatibility changes.

> Backfill software updates for September 2026 using `monthly-prompt.md`, with
> an entry date of September 30, 2026. Preserve existing entries and add only
> qualifying updates not already covered.

Optional overrides: topic focus, additional sources, maximum number of entries,
or **preview only** (research and present candidates without changing the database).

## Reusable prompt

Curate entries for **BBSR Omics Radar**, serving the University of Colorado
Cancer Center Biostatistics and Bioinformatics Shared Resource. Research the
requested period and add qualifying new entries to `data/omics_radar.duckdb`.

### Parameters and date rules

- Use the month or explicit date range in my request. Both endpoints are inclusive.
  If I omit the period, ask for it before researching.
- Use my requested entry date for **every** new record's `date_added`. If omitted,
  default to the last day of the requested period and state that assumption.
- The publication window and `date_added` serve different purposes. Select items
  by their verified publication/posting dates; do not use the entry date as proof
  that an item belongs in the window.
- Use the first online publication date for papers and the original posting date
  for blog posts. A substantive blog post published during the window qualifies
  even when its underlying paper is older. Record both the blog posting date and
  the paper's first online publication date, with separate evidence links; make
  clear when the post covers earlier research. A journal issue date, search-engine
  date, or routine webpage update does not establish eligibility.
- A substantial new software release or preprint revision can qualify by its own
  dated announcement/version. Identify what is new and distinguish it from the
  original publication. Do not duplicate an existing entry for a minor update.
- If a date cannot be verified, list the candidate as unresolved and do not insert
  it. Do not invent dates or include future publications.

### Scope and selection

Prioritize useful developments in bioinformatics, biostatistics, cancer research,
bulk and single-cell RNA-seq, spatial biology, multi-omics, reproducible analysis,
R/Python tooling, and AI/ML applied to biomedical research. Include relevant
technology platforms, research software security, and community resources.

Favor actionable methods, strong research findings, substantial software releases,
and practical tutorials. Explain the relevance to a bioinformatics or cancer
research team. Exclude generic technology news, advertising, routine patch releases
without material impact,
and unsupported claims. Label preprints and vendor claims clearly. Do not infer
clinical usefulness from preliminary or purely computational results.

Aim for about **15–25 strong entries** unless I specify otherwise. This is a target,
not a quota: add fewer when warranted, avoid padding, and report useful overflow.
Seek a mix of research, tools, and practical resources without forcing categories.

### Sources to scan

Scan each core source for the requested window. Use archives, RSS, journal listings,
and date-filtered searches as available; search snippets alone are not evidence.
Follow discovery links to original articles and official release announcements.
For RNA-seq Blog and other prolific sources, work through dated archive/category/
tag listings and pagination covering the whole requested period; do not stop at
the homepage. If archives fail, use multiple targeted searches and record the
remaining coverage gaps. Distinguish original post dates from modified timestamps.

| Core source | Focus |
| --- | --- |
| [RNA-seq Blog](https://www.rna-seqblog.com/) | Transcriptomics methods and news |
| [bioRxiv](https://www.biorxiv.org/) | Preprints in bioinformatics, genomics, cancer biology, and systems biology; use the official API and label preprints clearly |
| [Nature](https://www.nature.com/) | Relevant research, especially Nature Methods, Nature Biotechnology, Nature Genetics, Nature Cancer, and Nature Communications |
| [Science](https://www.science.org/) | Relevant research in Science, Science Advances, and Science Translational Medicine |
| [Python Weekly archives](https://www.pythonweekly.com/archive/) | Python tools and tutorials relevant to scientific work |
| [Planet Python](https://planetpython.org/) | Python community posts, scientific computing, and analysis tooling; verify dates on original posts |
| [R-bloggers](https://www.r-bloggers.com/) | R analysis, statistics, visualization, and packages |
| [Posit Open Source Blog](https://opensource.posit.co/blog/) | R/Python tooling and reproducible research |

Also scan these focused sources where relevant. Start with the repository's
README source list, supplemented by the sources below. Report which were checked.

| Additional source | Focus |
| --- | --- |
| [Bioconductor community blog](https://blog.bioconductor.org/) | Genomics packages, workflows, and community updates |
| [scverse blog](https://scverse.org/blog/) | Single-cell and spatial analysis tools |
| [nf-core blog](https://nf-co.re/blog) | Reproducible bioinformatics pipelines |
| [Ming Tang's blog](https://divingintogeneticsandgenomics.com/) | Practical genomics and single-cell tutorials |
| [Genome Biology](https://link.springer.com/journal/13059) | Genomics research and methods |
| [BMC Bioinformatics](https://link.springer.com/journal/12859) | Computational biology methods |
| [Bioinformatics](https://academic.oup.com/bioinformatics) | Algorithms and research software |
| [PLOS Computational Biology](https://journals.plos.org/ploscompbiol/) | Computational methods and reproducibility |
| [PyCoder's Weekly](https://pycoders.com/) | Additional Python discovery |

For relevant tools discovered during the search, inspect official project blogs,
release notes, or GitHub releases. Substantive blog coverage can qualify by its
own posting date; a bare aggregator/newsletter link cannot. Verify the underlying
research and record both dates. Prefer one entry for a development covered by
multiple sources, and do not re-add an existing paper solely for a later write-up.

### Software and AI product watchlist

**Check every required product below on every monthly run**, alongside the research
sources. Newsletters and blogs are discovery aids; they do not replace checking
official release histories. Keep this table as the maintained watchlist rather than
duplicating URLs elsewhere. Follow official redirects if a source moves.

| Required product | Official release sources | Changes of particular interest |
| --- | --- | --- |
| Python | [Release index](https://www.python.org/downloads/) and the linked version-specific release notes | Language/runtime capabilities, performance, scientific-package compatibility, support changes |
| R | [R NEWS](https://cran.r-project.org/doc/manuals/r-release/NEWS.html) | Statistical behavior, runtime changes, package compatibility, reproducibility |
| uv | [GitHub releases](https://github.com/astral-sh/uv/releases) | Environments, locking, dependency resolution, packaging, Python management |
| renv | [Changelog](https://rstudio.github.io/renv/news/index.html) | Lockfiles, restoration, repositories, portability, reproducibility |
| Nextflow | [GitHub releases](https://github.com/nextflow-io/nextflow/releases) | Workflow syntax, execution, containers, HPC/cloud support, migration requirements |
| RStudio | [RStudio / Workbench release notes](https://docs.posit.co/ide/news/index.html) | RStudio IDE changes; distinguish Workbench-only features and licensing |
| Positron | [Release notes](https://positron.posit.co/release-notes) and [GitHub releases](https://github.com/posit-dev/positron/releases) | R/Python analysis, notebooks, data exploration, debugging, assistants |
| VS Code | [Release archive](https://code.visualstudio.com/updates/archive) | Python/R development, notebooks, remote development, extensions, coding assistance |
| ChatGPT | [Release notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes) | Data/file analysis, research, collaboration, models, availability changes |
| Codex | [Product changelog](https://developers.openai.com/codex/changelog) | Coding and research workflows; distinguish desktop, CLI, IDE, cloud, and model changes |
| Claude | [Release notes](https://support.claude.com/en/articles/12138966-release-notes) | Analysis, research, artifacts, models, integrations, availability changes |
| Claude Code | [Official changelog](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md) | Coding workflows, tools, permissions, integrations, substantive reliability improvements |

Also check the following research-computing projects for substantial updates when
relevant to the requested scope. Record which were checked; these do not require
an entry when the month contains only routine maintenance.

| Additional project | Official release source |
| --- | --- |
| Bioconductor | [Release announcements](https://bioconductor.org/about/release-announcements/) |
| Quarto | [GitHub releases](https://github.com/quarto-dev/quarto-cli/releases) |
| Snakemake | [GitHub releases](https://github.com/snakemake/snakemake/releases) |
| nf-core pipelines | [Project news](https://nf-co.re/blog), then the specific pipeline's official release history |
| Scanpy / scverse | [Scanpy releases](https://github.com/scverse/scanpy/releases), plus relevant scverse package histories |
| Ruff | [GitHub releases](https://github.com/astral-sh/ruff/releases) |
| Polars | [GitHub releases](https://github.com/pola-rs/polars/releases) |
| DuckDB | [GitHub releases](https://github.com/duckdb/duckdb/releases) |

#### How to find and select software updates

1. **Enumerate the period.** Open each official changelog/release archive and
   inspect all dated releases in the requested window. Follow pagination; the
   latest release or RSS feed alone may omit earlier releases. Where useful, use
   the official repository's releases API and its published timestamps. Use
   date-filtered searches as a fallback and record retrieval gaps.
2. **Verify dates and availability.** Use the actual release/rollout date, not a
   marketing month label, tag commit date, page modification time, or today's
   latest version. An update labeled “September” but released in October belongs
   to October. Distinguish stable, beta, release candidate, nightly, and announced
   but not yet available features. For staged rollouts, record the stated start
   date and eligible plans/platforms; do not imply universal availability.
   If the changelog is undated, find a dated official announcement or release
   record; otherwise leave timing unresolved. A later blog recap does not redate
   a software release. A genuinely useful tutorial can qualify separately by its
   own posting date under the blog rules, with an explicit tutorial label.
3. **Select by impact.** Include major stable releases and meaningful features,
   breaking changes, deprecations, end-of-support notices, substantial performance
   improvements, and consequential fixes affecting security, data integrity,
   numerical correctness, or reproducibility. A patch can qualify on that basis;
   a major/minor version number alone is not sufficient. Describe vendor-reported
   performance as a claim unless independently assessed. Skip cosmetic changes,
   ordinary bug-fix churn, speculative roadmaps, and unreleased development notes.
   Include a preview only when unusually relevant, clearly labeled as a preview.
4. **Handle AI products separately.** Distinguish the chat product, coding agent,
   underlying model, and API. Confirm model availability for the specific product;
   an API launch does not prove the same model is in ChatGPT, Codex, or Claude Code.
   Include material retirements, access changes, or workflow changes; note plan,
   platform, region, and preview restrictions only where they affect the reader.
5. **Avoid release spam and duplicates.** Prefer one entry per coherent release
   or feature announcement. Several related releases of a fast-moving tool may
   be summarized together with their versions, individual dates, and evidence in
   the audit. Deduplicate by product + version/feature + channel against all
   existing entries and blog coverage. Use a version-specific URL or dated anchor
   rather than a rolling changelog homepage: the database requires unique URLs,
   and a shared homepage would collide with future months. If no stable distinct
   evidence URL exists, flag that limitation; do not invent tracking URLs to evade it.
6. **Explain practical value.** Write 2–3 sentences covering what changed, why
   it matters for the team's analysis/development workflow, and any material
   migration requirement or limitation. Use `Software & Tools`, `AI & Machine
   Learning`, or `Security` as appropriate, with a product tag and focused topic tags.
   Checking for updates means researching them, not installing or upgrading software.
7. **Audit every required product.** Record product, source checked, date span,
   versions/features considered, release date, channel, selection decision and
   reason, and any limitation. Use outcomes such as “added,” “already covered,”
   “no release found,” “only routine updates,” or “unable to verify.” Never treat
   a failed retrieval as “no release.” Record software versions and release dates
   in the audit without changing the database schema. Complete these checks even
   when the overall entry target has already been reached; report useful overflow.

### Source coverage lessons and fallback instructions

These notes reflect the September 2026 passes. Treat observed failures as limits
of those retrieval attempts, not proof that a source is permanently unavailable.

- **bioRxiv:** It was optional in the first pass; a targeted search found a PBMC
  reference candidate, but its landing page failed to open and no API fallback
  was attempted. Narrow `site:` searches also returned no results in the follow-up,
  while broader searches and the official API found relevant September material.
  Start with [API documentation](https://api.biorxiv.org/) and enumerate the exact
  requested interval, for example
  `https://api.biorxiv.org/details/biorxiv/2026-09-01/2026-09-30/0?category=bioinformatics`.
  Scan bioinformatics, genomics, cancer_biology, and systems_biology; add other
  categories for the requested topic. Follow pagination to the reported total
  (currently 30 records per details call), validate returned dates, and record
  fetched counts and any missing pages. A complete metadata retrieval is not a
  full-text review of every paper. Use title/abstract screening, then read selected
  abstracts or manuscripts. If a landing page fails, an official API abstract is
  usable primary evidence; disclose abstract-only access and save the evidence.
  The monthly directory at `https://connect.biorxiv.org/archive/` is another
  discovery route, but September's full page exceeded the web reader's size limit.
  Read actual version posting dates, never the date-like string inside a DOI.
  Query selected DOIs for version history; distinguish first postings from revisions,
  keep the version reviewed, and check linked journal DOIs for existing entries.
  Do not call revisions new studies or assume the API's missing journal link proves
  a manuscript has never been peer reviewed. Label the curated version a preprint.
- **RNA-seq Blog:** The first pass relied on the homepage and a few links, missing
  relevant posts. Direct archive/tag opens sometimes returned stale snapshots,
  and some primary links failed. Check dated listings across the entire month,
  cross-check multiple retrieval routes, and state evidence limitations. The initial
  interpretation also excluded timely posts about older papers; the user clarified
  that substantive monthly blog coverage qualifies. Record both dates and the
  discovery source, even when linking the primary paper, so its contribution is visible.
- **Other aggregators and publishers:** September R-bloggers archives and several
  publisher pages could not be retrieved. Python Weekly supplied discovery links,
  but a linked Quansight article could not be read. Try official RSS, issue/category
  archives, publisher metadata, and author/project pages before marking unresolved.
  Do not equate a failed page or empty search with no relevant publications.
- **Across sources:** Give every core source a coverage status before stopping:
  checked, partial, or inaccessible. Log retrieval route, date span, candidates
  considered, selected items, unresolved candidates, and reasons for exclusion.
  Source names in the list alone do not demonstrate coverage. The 15–25 target
  must not stop source checks; surface strong overflow or include it when requested.
- **Software:** Earlier passes found some Posit releases through blog posts, but
  had no product-by-product release checklist. This left other tools' coverage
  unestablished. Check the watchlist directly and record an outcome per product;
  do not infer absence of updates from absence of newsletter or blog coverage.
  In the September software backfill, VS Code's archive returned an old listing
  while version-specific pages and the official GitHub releases API contained
  September releases. Positron's main release-notes page showed only the newest
  month. Cross-check these sources against versioned records, and distinguish
  release dates from later blog coverage before adding duplicates.
  Claude's help-center page returned 403 locally and stale content through the
  web reader, despite newer search snippets. Use dated official Claude/Anthropic
  announcements and the Claude Code release history as fallbacks; report app
  coverage as partial when the full monthly history cannot be enumerated.
  OpenAI's current unified [product changelog](https://learn.chatgpt.com/docs/changelog)
  and dated announcements can supplement older ChatGPT/Codex release links.
  Follow sparse release notes into their linked backport PRs when needed (as
  with Polars 1.44.2). Record preview flags from release metadata: a version number
  alone does not establish stability. Include consequential patch fixes, such as
  query correctness or unsafe automatic code rewrites, without treating every
  maintenance release as a separate entry.

### Research and prepare entries

1. Read repository instructions, `README.md`, and the current database helpers in
   `src/omics_radar/database.py`. Inspect existing entries across **all dates** for
   duplicates and established tag conventions.
2. Build a candidate list with title, canonical URL, verified publication date,
   date-evidence link, source, category, tags, and a concise original summary.
   Record the discovery source and URL separately from the primary publication.
   For blog coverage, also record the blog date, underlying paper date and URL,
   and which date establishes eligibility. Link the blog when curating its coverage.
   If only an abstract is accessible, summarize only what it supports and note
   the access limitation. Do not bypass access restrictions.
3. Deduplicate against both the database and the candidate list. Check canonical
   URLs, DOI, normalized titles, and the underlying paper/tool announcement.
   Remove tracking parameters without removing meaningful URL parameters. Treat
   syndication, preprint/journal versions, and multiple write-ups as potential
   duplicates, even if URLs differ.
4. Give each entry a faithful, readable title and a **2–3 sentence summary** of
   what is new and why it matters. Include material limitations or preprint status.
   Paraphrase; do not copy abstracts or marketing text.
5. Choose exactly one category from the current `PRIMARY_CATEGORIES` constant:
   `Software & Tools`, `Cancer Research`, `AI & Machine Learning`,
   `Technology Platforms`, `Security`, `Community`, or `Other`.
   Add 2–5 focused tags, reusing existing spelling and capitalization where possible.

### Insert and verify

- Unless I requested preview only, proceed with adding verified qualifying entries.
  Preserve existing entries and published reports; do not publish a newsletter,
  regenerate `docs/`, commit, or push as part of this curation request.
- Make a recoverable local database backup before writing, with no active writer.
  Use the repository's `create_article` helper and supported setup/runtime. If the
  database is locked, report the blocker rather than terminating another process.
- Supply `title`, `summary`, `date_added`, `url`, `primary_category`, and `tags`.
  Let the helper generate IDs and actual creation/update timestamps. Do not
  backdate those timestamps or change the schema. Publication dates and evidence
  belong in the final audit table because the current schema has no publication-date field.
- Record inserted IDs. If a run partially succeeds, report exactly what was added
  and what failed; check again for duplicates before retrying.
- Read inserted records back and verify their count, requested `date_added`, URLs,
  summaries, categories, and tags. Confirm existing records were preserved.

### Completion report

Return:

1. Publication window, assigned entry date, and counts added/skipped/unresolved.
2. An audit table of added entries: ID, linked title, source, verified publication
   date with evidence link, `date_added`, category, and tags. Show discovery source
   and both blog/paper dates where applicable, so source contributions are visible.
3. Source coverage: sources checked, qualifying items found, and any access or
   archive limitations. Distinguish “no qualifying items found” from “unable to check.”
   Include the software watchlist audit with an outcome for every required product,
   selected release versions/dates, availability restrictions, and skipped-update reasons.
4. Notable duplicates, uncertain dates, excluded candidates, and useful overflow,
   with short reasons. Identify the backup location and any partial failures.

For preview only, return the proposed entries including summaries and the same
evidence and coverage information, and leave the database unchanged.
