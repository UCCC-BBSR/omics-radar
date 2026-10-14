# BBSR Omics Radar

Static site located at:

https://uccc-bbsr.github.io/omics-radar/index.html

A local Streamlit editorial application and static newsletter publisher for the
University of Colorado Cancer Center Biostatistics and Bioinformatics Shared
Resource.

## Run locally

```bash
uv sync
uv run streamlit run app.py
```

The app creates its local database at `data/omics_radar.duckdb`. The database is
pushed to GitHub. Database could be split in the future if it gets too big. Add and manage entries locally, then publish an issue to write
the public site to `docs/`.

## Test

```bash
uv run pytest
```

## Sources list:

- [Bioinformatics (Springer)](https://link.springer.com/journal/12859)
- [Bioinformatics Blogs Aggregator](https://bioinf-bloggers.com)
- [Genome Biology](https://link.springer.com/journal/13059)
- [Ming Tang Blog](https://divingintogeneticsandgenomics.com/)
- [Nature Methods - Comp Bio](https://www.nature.com/subjects/computational-biology-and-bioinformatics/nmeth)
- [PLOS Computational Biology](https://journals.plos.org/ploscompbiol/)
- [Planet Python](https://planetpython.org/)
- [Posit Open Source Blog](https://opensource.posit.co/blog/)
- [Python Bytes Podcast](https://pythonbytes.fm/)
- [R Bloggers](https://www.r-bloggers.com/)
- [RNA-seq Blog](https://www.rna-seqblog.com/)
- [bioRxiv](https://www.biorxiv.org/) — bioinformatics, genomics, cancer biology, and systems biology preprints; [official metadata API](https://api.biorxiv.org/)

Use [monthly-prompt.md](monthly-prompt.md) for monthly curation, including source
coverage checks, date rules, and lessons from earlier retrieval gaps.

Monthly software checks cover **Python, R, uv, renv, Nextflow, RStudio, Positron,
VS Code, ChatGPT, Codex, Claude, and Claude Code**. The
[software watchlist](monthly-prompt.md#software-and-ai-product-watchlist) contains
official release sources, additional research-computing projects, and criteria
for selecting meaningful updates and recording coverage.


See [implementation.md](implementation.md) for the architecture, data model,
workflow, and roadmap.
