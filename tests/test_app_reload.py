from pathlib import Path

from streamlit.testing.v1 import AppTest

from omics_radar import issue_selection


def test_app_recovers_from_stale_issue_renderer(tmp_path, monkeypatch):
    # Reproduce a long-running server retaining the renderer's old signature.
    def old_renderer(candidates, *, scope):
        raise AssertionError('The stale renderer must not be used')

    monkeypatch.setattr(issue_selection, 'select_issue_entries', old_renderer)
    root = Path(__file__).resolve().parents[1]
    script = (root / 'app.py').read_text().replace(
        'ROOT = Path(__file__).resolve().parent', f'ROOT = Path({str(root)!r})'
    ).replace(
        'DATABASE_PATH = ROOT / "data" / "omics_radar.duckdb"',
        f'DATABASE_PATH = Path({str(tmp_path / "test.duckdb")!r})',
    )
    app = AppTest.from_string(script).run()
    assert not app.exception
    assert len(app.tabs) == 3
    app.run()
    assert not app.exception
