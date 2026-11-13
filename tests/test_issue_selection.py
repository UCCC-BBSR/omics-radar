from streamlit.testing.v1 import AppTest


SCRIPT = """
import streamlit as st
from omics_radar.issue_selection import select_issue_entries

candidates = [
    dict(id='a', title='A long research title that must remain readable in full',
         summary='Detailed description of a single-cell cancer study.',
         date_added='2026-10-31', url='https://example.org/a',
         primary_category='Cancer Research', tags=['single cell']),
    dict(id='b', title='Python analysis toolkit', summary='Reproducible workflows.',
         date_added='2026-10-31', url='https://example.org/b',
         primary_category='Software & Tools', tags=['python']),
]
scope = st.selectbox('Issue', ['October', 'November'])
st.session_state['chosen'] = select_issue_entries(candidates, scope=scope)
"""


def test_entries_are_readable_and_exclusions_survive_filtering():
    app = AppTest.from_string(SCRIPT).run()
    assert not app.exception
    assert app.session_state['chosen'] == ['a', 'b']
    text = '\n'.join(element.value for element in app.markdown)
    assert 'A long research title that must remain readable in full' in text
    assert 'Detailed description of a single-cell cancer study.' in text

    app.checkbox[0].uncheck().run()
    assert app.session_state['chosen'] == ['b']
    app.text_input[0].set_value('python').run()
    assert len(app.checkbox) == 1
    assert app.session_state['chosen'] == ['b']
    app.text_input[0].set_value('').run()
    assert not app.checkbox[0].value
    assert app.session_state['chosen'] == ['b']
    assert not app.exception


def test_bulk_actions_only_change_visible_entries():
    app = AppTest.from_string(SCRIPT).run()
    app.selectbox[1].select('Software & Tools').run()
    app.button[1].click().run()  # Exclude all shown
    assert app.session_state['chosen'] == ['a']
    app.selectbox[1].select('All categories').run()
    assert [c.value for c in app.checkbox] == [True, False]
    app.button[0].click().run()  # Include all shown
    assert app.session_state['chosen'] == ['a', 'b']
    app.text_input[0].set_value('no matching entry').run()
    assert not app.checkbox
    assert all(button.disabled for button in app.button)
    assert app.session_state['chosen'] == ['a', 'b']
    assert not app.exception


def test_issue_selections_are_independent_and_survive_switching():
    app = AppTest.from_string(SCRIPT).run()
    app.checkbox[0].uncheck().run()
    app.selectbox[0].select('November').run()
    assert app.session_state['chosen'] == ['a', 'b']
    app.selectbox[0].select('October').run()
    assert app.session_state['chosen'] == ['b']
    assert not app.checkbox[0].value
    assert not app.exception


def test_empty_issue():
    app = AppTest.from_string('''
from omics_radar.issue_selection import select_issue_entries
assert select_issue_entries([], scope='empty') == []
''').run()
    assert not app.exception
    assert 'No entries' in app.info[0].value


def test_inline_edits_save_to_database_and_preserve_selection(tmp_path):
    from datetime import date
    from omics_radar.database import create_article, get_article, initialize_database

    path = tmp_path / 'editor.duckdb'
    initialize_database(path)
    article_id = create_article(
        path, title='Original title', summary='Original summary', date_added=date(2026, 10, 31),
        url='https://example.org/edit', primary_category='Cancer Research', tags=['original'],
    )
    before = get_article(path, article_id)
    app = AppTest.from_string(f'''
import streamlit as st
from omics_radar.database import list_articles
from omics_radar.issue_selection import select_issue_entries
path = {str(path)!r}
articles = list_articles(path)
st.session_state['chosen'] = select_issue_entries(articles, scope='October', database_path=path)
''').run()
    app.checkbox[0].uncheck().run()
    app.text_input[1].set_value('  Revised title  ')
    app.text_area[0].set_value('Revised summary')
    app.text_input[2].set_value('RNA-seq, cancer, RNA-seq')
    app.button[2].click().run()
    assert not app.exception
    saved = get_article(path, article_id)
    assert saved['title'] == 'Revised title'
    assert saved['summary'] == 'Revised summary'
    assert saved['tags'] == ['cancer', 'RNA-seq']
    for field in ('id', 'url', 'date_added', 'primary_category', 'created_at'):
        assert saved[field] == before[field]
    assert app.session_state['chosen'] == []
    assert 'Revised title' in '\n'.join(e.value for e in app.markdown)
    assert app.success
    assert app.text_input[1].value == 'Revised title'

    # Invalid input remains editable without changing the stored entry.
    app.text_input[1].set_value('   ')
    app.button[2].click().run()
    assert not app.exception
    assert app.error[0].value == 'Title is required.'
    assert get_article(path, article_id) == saved
    assert app.text_area[0].value == 'Revised summary'
    app.text_input[1].set_value('Revised title')
    app.text_area[0].set_value('')
    app.button[2].click().run()
    assert app.error[0].value == 'Summary is required.'
    assert get_article(path, article_id) == saved
