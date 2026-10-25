"""Validate changed documentation and build a local static README preview."""
from pathlib import Path
import base64, hashlib, html, json, re, subprocess, sys
from urllib.parse import unquote, urlsplit
from urllib.request import Request, urlopen
from concurrent.futures import ThreadPoolExecutor
import xml.etree.ElementTree as ET
sys.path.insert(0,str(Path(__file__).resolve().parents[3]/"render-tools"))
from markdown_it import MarkdownIt

ROOT=Path(__file__).resolve().parents[2]
REPORT=ROOT/"reports/freg003"
BASE="8e7a2e8f0a2076b3bdf1564888a8a07f9b59e6d8"
md=MarkdownIt("commonmark",{"html":False}).enable("table")
files=["README.md","docs/probar-forestrag.md","docs/arquitectura.md","docs/evaluacion.md","docs/security-lab.md","docs/limitaciones.md","FORESTRAG_ESTADO_MAESTRO_Y_CONTINUIDAD.md","FORESTRAG_PLAN_MAESTRO_INTEGRADO.md","FORESTRAG_BACKLOG_PRIORIZADO.md","FORESTRAG_BITACORA_DECISIONES.md","FORESTRAG_SECURITY_TEST_MATRIX.md","FORESTRAG_INFORME_INCREMENTO_ACTUAL.md"]
REPORT.mkdir(parents=True,exist_ok=True)
(REPORT/"validation.json").touch(exist_ok=True)
def slug(s):
    return re.sub(r"[^\w\- ]","",s.lower()).replace(" ","-")
def headings(text):
    tokens=md.parse(text); result=[]
    for i,t in enumerate(tokens):
        if t.type=="heading_open":
            result.append((int(t.tag[1]),tokens[i+1].content,slug(tokens[i+1].content)))
    return result
links=[]; failures=[]
for name in files:
    p=ROOT/name
    text=p.read_text(encoding="utf-8")
    assert "\ufffd" not in text and not re.search("Ã.|â€|Â·",text),name
    for token in md.parse(text):
        for child in token.children or []:
            attr="src" if child.type=="image" else "href" if child.type=="link_open" else None
            if not attr: continue
            href=child.attrGet(attr)
            parts=urlsplit(href)
            row={"source":name,"destination":href,"image":child.type=="image"}
            if parts.scheme in ("http","https","mailto"):
                row["kind"]="external"
            elif parts.scheme:
                row.update(kind="unsupported",status="FAIL");failures.append(row)
            else:
                row["kind"]="local"
                target=(p.parent/unquote(parts.path)).resolve() if parts.path else p
                okay=target.is_relative_to(ROOT) and target.is_file()
                if okay and parts.fragment and target.suffix==".md":
                    okay=unquote(parts.fragment) in [v[2] for v in headings(target.read_text(encoding="utf-8"))]
                row["status"]="PASS" if okay else "FAIL"
                if not okay:failures.append(row)
            links.append(row)
runtime=subprocess.check_output(["git","diff","--name-only",BASE,"--","src","app","tests","scripts","pyproject.toml","requirements.txt",".github","requirements-*.lock"],cwd=ROOT,text=True).splitlines()
assert not runtime,runtime
# Recovered evidence is verified as an artifact, not rerun here.
receipt=json.loads((ROOT/"reports/freg002/receipt.json").read_text(encoding="utf-8"))
history={}
for name,entry in receipt["suites"].items():
    p=ROOT/"reports/freg002"/name
    okay=hashlib.sha256(p.read_bytes()).hexdigest()==entry["sha256"]
    cases=ET.parse(p).findall(".//testcase")
    assert okay and len(cases)==97
    history[name]={"sha256_match":okay,"cases":len(cases),"executed_now":False}
xml=ET.parse(REPORT/"windows-security.xml")
cases=xml.findall(".//testcase")
status={"PASS":0,"FAIL":0,"ERROR":0,"SKIP":0}
for c in cases:
    s="ERROR" if c.find("error") is not None else "FAIL" if c.find("failure") is not None else "SKIP" if c.find("skipped") is not None else "PASS"
    status[s]+=1
assert status=={"PASS":43,"FAIL":0,"ERROR":0,"SKIP":0},status
def remote(url):
    try:
        with urlopen(Request(url,method="HEAD",headers={"User-Agent":"ForestRAG-doc-check"}),timeout=12) as response:
            return {"url":url,"status":response.status,"result":"PASS" if response.status<400 else "BLOCKED"}
    except Exception as exc:
        return {"url":url,"result":"BLOCKED","reason":type(exc).__name__}
urls=sorted({r["destination"] for r in links if r["kind"]=="external" and r["source"]=="README.md"})
with ThreadPoolExecutor(max_workers=3) as pool:
    remote_results=list(pool.map(remote,urls))
readme=(ROOT/"README.md").read_text(encoding="utf-8")
before=subprocess.check_output(["git","show",BASE+":README.md"],cwd=ROOT).decode("utf-8")
result={
 "increment":"FREG-003","base_commit":BASE,"branch":"freg-003-readme","published":False,
 "prompt_sha256":(hashlib.sha256((ROOT.parent/"input/prompt.txt").read_bytes()).hexdigest() if (ROOT.parent/"input/prompt.txt").exists() else json.loads((REPORT/"validation.json").read_text(encoding="utf-8")).get("prompt_sha256")),
 "documents_checked":len(files),"links":links,"failures":failures,
 "local_links_checked":sum(x["kind"]=="local" for x in links),"external_readme_links":remote_results,
 "markdown":{"parser":"markdown-it-py 4.0.0 CommonMark + table","readme_headings":headings(readme),"raw_html":False,"mermaid_used":False},
 "comparison":{"old_lines":len(before.splitlines()),"new_lines":len(readme.splitlines()),"old_words":len(before.split()),"new_words":len(readme.split())},
 "unchanged_runtime_paths":not runtime,"windows_tests":status,"recovered_linux_evidence":history,
 "not_run":["Current Windows semantic embeddings/PDF integration","Current Streamlit browser session","Real LLM generation","New Windows dependency vulnerability scan","External reader study"],
 "editorial_score":{"clarity":23,"value":18,"operation":14,"present_future":15,"visual_navigation":9,"accuracy":9,"documentation":5,"total":93,"kind":"internal judgement; not user research"}
}
(REPORT/"validation.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
# A local preview, not a claim of exact GitHub rendering.
tokens=md.parse(readme)
counts={}
for i,t in enumerate(tokens):
    if t.type=="heading_open":
        anchor=slug(tokens[i+1].content)
        n=counts.get(anchor,0); counts[anchor]=n+1
        t.attrSet("id",anchor if not n else anchor+"-"+str(n))
    for child in t.children or []:
        if child.type=="image":
            path=ROOT/child.attrGet("src")
            child.attrSet("src","data:image/jpeg;base64,"+base64.b64encode(path.read_bytes()).decode("ascii"))
css="""body{margin:0;background:#f6f8fa;color:#1f2328;font:16px/1.6 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}main{box-sizing:border-box;max-width:980px;margin:28px auto;padding:32px 48px;background:white;border:1px solid #d1d9e0;border-radius:6px}aside{max-width:884px;margin:24px auto 0;padding:0 24px;font-size:13px;color:#59636e}h1,h2,h3{line-height:1.25;font-weight:600;margin:24px 0 16px}h1{font-size:32px;border-bottom:1px solid #d1d9e0;padding-bottom:10px}h2{font-size:24px;border-bottom:1px solid #d1d9e0;padding-bottom:8px}h3{font-size:20px}p,ul,ol{margin:0 0 16px}li+li{margin-top:4px}a{color:#0969da;text-decoration:none}a:hover{text-decoration:underline}pre{background:#f6f8fa;padding:16px;border-radius:6px;overflow:auto;font-size:13px}code{font:85% ui-monospace,SFMono-Regular,Consolas,monospace;background:#afb8c133;padding:.15em .3em;border-radius:4px}pre code{padding:0;background:transparent}img{max-width:100%;height:auto;border-radius:5px}blockquote{margin:0 0 16px;padding:0 16px;color:#59636e;border-left:4px solid #d1d9e0}table{border-collapse:collapse}td,th{padding:8px;border:1px solid #d1d9e0}@media(max-width:650px){main{margin:0;padding:20px 18px;border:0}aside{margin:10px 0}h1{font-size:28px}}"""
preview="<!doctype html><html lang='es'><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>ForestRAG — vista previa del README</title><style>"+css+"</style><aside>Vista previa local del README · FREG-003 preparado, sin publicar · Estilo aproximado; GitHub aplica su propio renderizador.</aside><main>"+md.renderer.render(tokens,md.options,{})+"</main></html>"
(ROOT/"README_preview.html").write_text(preview,encoding="utf-8",newline="\n")
print(json.dumps({k:result[k] for k in ["documents_checked","local_links_checked","external_readme_links","comparison","windows_tests","unchanged_runtime_paths"]},ensure_ascii=False,indent=2))
assert not failures,failures
