# BBSR Omics Radar

A local Streamlit editorial application and static newsletter publisher for the
University of Colorado Cancer Center Biostatistics and Bioinformatics Shared
Resource.

## Run locally

```bash
uv sync
uv run streamlit run app.py
```

The app creates its local database at `data/omics_radar.duckdb`. The database is
ignored by Git. Publishing an issue writes the public site to `docs/`.

## Test

```bash
uv run pytest
```

See [implementation.md](implementation.md) for the architecture, data model,
workflow, and roadmap.
