import argparse
import json
from pathlib import Path

from .embeddings import make_embedder
from .evaluation import evaluate
from .generation import extractive_answer, ollama_answer, risky_request
from .ingestion import load_sources, read_source
from .preprocessing import chunk_pages
from .retrieval import retrieve
from .vector_store import write_index


def build_index(manifest, raw_dir, path, embedder):
    sources = load_sources(Path(manifest))
    pages = [p for s in sources for p in read_source(s, Path(raw_dir))]
    chunks = chunk_pages(pages, token_count=embedder.token_count)
    vectors = embedder.encode([c.text for c in chunks])
    fingerprint = write_index(Path(path), chunks, vectors, embedder.id)
    return {"sources": len(sources), "pages": len(pages), "chunks": len(chunks),
            "dimensions": vectors.shape[1], "embedder": embedder.id, "index_sha256": fingerprint}


def main():
    parser = argparse.ArgumentParser(description="ForestRAG: recuperación documental trazable")
    parser.add_argument("command", choices=["ingest", "ask", "evaluate", "demo"])
    parser.add_argument("--backend", choices=["semantic", "lexical"], default="semantic")
    parser.add_argument("--index", type=Path, default=Path("data/forest.db"))
    parser.add_argument("--manifest", type=Path, default=Path("examples/sources.json"))
    parser.add_argument("--raw-dir", type=Path, default=Path("data/raw"))
    parser.add_argument("--question")
    parser.add_argument("--cases", type=Path, default=Path("examples/evaluation_fao.json"))
    parser.add_argument("--threshold", type=float, default=0.5)
    parser.add_argument("--k", type=int, default=3)
    parser.add_argument("--llm", action="store_true")
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "demo":
            embedder = make_embedder("lexical")
            path = Path("data/demo.db")
            built = build_index("examples/demo_sources.json", "examples/corpus", path, embedder)
            hits = retrieve(args.question or "¿Qué campos contiene una orden de mantenimiento?",
                            path, embedder, threshold=0.25, trusted_sha256=built["index_sha256"])
            result = extractive_answer(hits)
        else:
            embedder = make_embedder(args.backend)
            if args.command == "ingest":
                result = build_index(args.manifest, args.raw_dir, args.index, embedder)
            elif args.command == "ask":
                if risky_request(args.question or ""):
                    result = {"abstained": True, "message": "Consulte procedimientos oficiales y personal autorizado."}
                else:
                    hits = retrieve(args.question, args.index, embedder, args.k, args.threshold)
                    result = ollama_answer(args.question, hits) if args.llm else extractive_answer(hits)
            else:
                cases = json.loads(args.cases.read_text(encoding="utf-8"))
                result = evaluate(cases, args.index, embedder, args.k, args.threshold)
        output = json.dumps(result, ensure_ascii=False, indent=2)
        if args.out:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(output + "\n", encoding="utf-8")
        print(output)
    except (ValueError, RuntimeError, OSError) as exc:
        parser.exit(2, f"ForestRAG: {exc}\n")


if __name__ == "__main__":
    main()

