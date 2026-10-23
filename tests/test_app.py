from pathlib import Path

from streamlit.testing.v1 import AppTest


def test_query_ui_uses_real_local_index(index, monkeypatch):
    path, _ = index
    monkeypatch.setenv("FORESTRAG_INDEX", str(path))
    app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / "app/streamlit_app.py"))
    app.run(timeout=20)
    assert not app.exception
    app.text_input[0].input("orden mantenimiento equipo")
    app.button[0].click().run()
    assert not app.exception
    assert any("No es una respuesta generada" in str(x.value) for x in app.markdown)
    assert len(app.expander) >= 1


def test_missing_index_is_explained(tmp_path, monkeypatch):
    monkeypatch.setenv("FORESTRAG_INDEX", str(tmp_path / "missing.db"))
    app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / "app/streamlit_app.py")).run()
    assert not app.exception and len(app.warning) == 1

