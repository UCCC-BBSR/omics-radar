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
ignored by Git. Add and manage entries locally, then publish an issue to write
the public site to `docs/`.

## Test

```bash
uv run pytest
```

See [implementation.md](implementation.md) for the architecture, data model,
workflow, and roadmap.
