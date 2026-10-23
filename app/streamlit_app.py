"""Interfaz local sin cargas de archivos ni llamadas a proveedores externos."""
import os
from pathlib import Path

import streamlit as st

from forestrag.embeddings import make_embedder
from forestrag.generation import extractive_answer, ollama_answer, risky_request
from forestrag.retrieval import retrieve
from forestrag.vector_store import index_metadata

st.set_page_config(page_title="ForestRAG", page_icon="🌲", layout="wide")
st.title("ForestRAG")
st.caption("Asistente Documental Forestal · Prototipo personal de Ignacio Pizarro Hurtado")
st.info("Proyecto independiente, sin afiliación ni respaldo de ARAUCO. Consulte siempre las fuentes oficiales.")
st.markdown("### Consulta documental")
index = Path(os.environ.get("FORESTRAG_INDEX", "data/forest.db"))
try:
    metadata = index_metadata(index)
except (ValueError, OSError):
    st.warning("Prepare el índice con la guía del README antes de consultar.")
    st.stop()
backend = "lexical" if metadata["embedder"].startswith("lexical") else "semantic"
st.caption("Búsqueda semántica local" if backend == "semantic" else "Demostración léxica con material ficticio")
question = st.text_input("Pregunta sobre el corpus", max_chars=1000,
                         placeholder="¿Cómo ayuda la inteligencia artificial a analizar datos de teledetección?")
use_llm = st.checkbox("Usar Ollama local (experimental; requiere instalación y modelo)", value=False)
st.caption("El modo predeterminado muestra fragmentos. Las similitudes no son probabilidades de certeza.")

@st.cache_resource
def get_embedder(name):
    return make_embedder(name)

if st.button("Consultar", type="primary"):
    try:
        if risky_request(question):
            st.warning("Consulte el procedimiento oficial y a personal autorizado.")
        else:
            with st.spinner("Buscando evidencia..."):
                hits = retrieve(question, index, get_embedder(backend),
                                threshold=0.5 if backend == "semantic" else 0.25)
                result = ollama_answer(question, hits) if use_llm else extractive_answer(hits)
            st.write(result["message"])
            for claim in result.get("claims", []):
                st.write(claim["text"])
                st.caption("Referencias: " + ", ".join(claim["citations"]))
            for n, hit in enumerate(hits, start=1):
                with st.expander(f"{n}. {hit.chunk.title} · página PDF {hit.chunk.page}", expanded=n == 1):
                    st.text(hit.chunk.text)
                    st.caption(f"Página rotulada: {hit.chunk.page_label} · ID: {hit.chunk.id} · coseno: {hit.score:.3f}")
                    st.link_button("Abrir fuente", hit.chunk.url + f"#page={hit.chunk.page}")
    except (ValueError, RuntimeError, OSError) as exc:
        st.error(str(exc))
st.caption("Consulta experimental. Sin certificación de seguridad operacional. No sustituye instrucciones del fabricante.")

