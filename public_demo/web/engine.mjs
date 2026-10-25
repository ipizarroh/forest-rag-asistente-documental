export const ENGINE = "lexical-sha256-512-v1";
const STOP = new Set("que una uno unos unas como cual cuales donde cuando esto esta este estas estos para por con sin del las los sus sobre antes cada puede pueden".split(" "));
const invalid = () => { throw new Error("El corpus no supera la validación."); };
export function validateBundle(data) {
  if (!data || data.schema_version !== 1 || data.engine !== ENGINE ||
      !Array.isArray(data.documents) || !data.documents.length || data.documents.length > 12 ||
      !Array.isArray(data.chunks) || !data.chunks.length || data.chunks.length > 200) invalid();
  const docs = new Map(), ids = new Set();
  for (const d of data.documents) {
    if (!d || typeof d.id !== "string" || !/^[a-z][a-z0-9-]{1,40}$/.test(d.id) || docs.has(d.id) ||
        d.classification !== "public" || d.synthetic !== true || d.approved_for_public_demo !== true ||
        d.status !== "active" || !Number.isInteger(d.version) || d.version < 1 ||
        d.license !== "CC0-1.0" || typeof d.title !== "string" || d.title.length > 120 ||
        !Array.isArray(d.sections) || !d.sections.length || d.sections.length > 8 ||
        !/^[a-f0-9]{64}$/.test(d.sha256)) invalid();
    for (const s of d.sections) if (!s || typeof s.text !== "string" || !s.text.trim() ||
      s.text.length > 4000 || typeof s.title !== "string" || s.title.length > 120) invalid();
    docs.set(d.id, d);
  }
  for (const c of data.chunks) {
    if (!c || typeof c.id !== "string" || !/^[a-f0-9]{24}$/.test(c.id) || ids.has(c.id) ||
        !docs.has(c.document_id) || !Number.isInteger(c.section) || c.section < 1 ||
        c.section > docs.get(c.document_id).sections.length ||
        typeof c.text !== "string" || !c.text.trim() || c.text.length > 4000 ||
        typeof c.section_title !== "string" || c.section_title !== docs.get(c.document_id).sections[c.section-1].title ||
        !docs.get(c.document_id).sections[c.section-1].text.replace(/\s+/g," ").includes(c.text) ||
        !Array.isArray(c.vector) || !c.vector.length || c.vector.length > 512) invalid();
    let norm = 0; const buckets = new Set();
    for (const pair of c.vector) {
      if (!Array.isArray(pair) || pair.length !== 2) invalid();
      const [i,v] = pair;
      if (!Number.isInteger(i) || i < 0 || i >= 512 || buckets.has(i) ||
          typeof v !== "number" || !Number.isFinite(v) || v <= 0 || v > 1) invalid();
      buckets.add(i); norm += v*v;
    }
    if (Math.abs(norm-1) > 1e-5) invalid();
    ids.add(c.id);
  }
  return data;
}
export function terms(text) {
  return text.toLowerCase().normalize("NFD").replace(/\p{Mn}/gu,"")
    .match(/(?<![\p{L}\p{N}_])[a-z0-9]{3,}(?![\p{L}\p{N}_])/gu) || [];
}
export async function encodeQuery(question) {
  if (typeof question !== "string" || !question.trim() || question.length > 320)
    throw new Error("Escribe una consulta de 1 a 320 caracteres.");
  const tokens = terms(question);
  if (!tokens.length || tokens.length > 64) throw new Error("Usa palabras de al menos 3 letras; máximo 64 palabras.");
  const vector = new Float32Array(512);
  const hashes = await Promise.all(tokens.map(t => crypto.subtle.digest("SHA-256", new TextEncoder().encode(t))));
  for (const h of hashes) vector[new DataView(h).getUint32(0,false)%512]++;
  const norm = Math.sqrt(vector.reduce((s,v)=>s+v*v,0));
  return vector.map(v=>v/norm);
}

// Limited corpus vocabulary, not semantic inference or a general Spanish stemmer.
const GROUPS = [
  ["registro","registra","registran","registrar","registros","anota","anotar"],
  ["observacion","observaciones"],["campo","campos","datos"],
  ["imagen","imagenes"],["fotografia","fotografias","fotos"],
  ["retira","retirar","retirado","retirada","retiro","quitar"],
  ["version","versiones"],["revisa","revisan","revisar","revision","revisiones"],
  ["compara","comparar","comparacion","comparaciones"],["documento","documentos"],
  ["fecha","fechas"]
];
const ALIASES = new Map(GROUPS.flatMap(group=>group.map(t=>[t,group[0]])));
const SEARCH_STOP = new Set([...STOP,...terms("quien tiene tienen puedo podemos hay aqui este esta aplicacion demo del los las una que para porque informacion favor quiero necesito saber encontrar hace hacer hago encuentra")]);
SEARCH_STOP.delete("antes"); // Preserve temporal conditions that distinguish preparation from comparison.
export function searchTerms(text) {
  return terms(text).filter(t=>!SEARCH_STOP.has(t)).map(t=>(ALIASES.get(t)??t).replace(/ciones$/,'cion').replace(/(?<=.{4})s$/,''));
}
export function isCatalogQuery(question) {
  const t=terms(question).join(" ");
  const target=/\b(forestrag|aplicacion|sistema)\b/.test(t);
  const catalog=/\b(catalogo|temas|documentos|informacion|consultar|consulta|contiene|capacidades)\b/.test(t);
  const navigation=/\b(que|cuales|puedo|hay|disponibles|encontrar|explorar|trata|funciona|hacer|sirve)\b/.test(t);
  // Restrict orientation to general navigation; factual questions still retrieve evidence.
  const factual=/\b(campos|registra|observacion|imagenes|retira|version|fecha|revision|sha|comparar|documento)\b/.test(t);
  return navigation && !factual && (catalog || target);
}
export const suggestions = [
  {question:"¿Qué puedo encontrar en ForestRAG?",documentId:""},
  {question:"¿Qué campos registra una observación de terreno?",documentId:"registro-terreno"},
  {question:"¿Qué se revisa antes de comparar imágenes?",documentId:"monitoreo-forestal"},
  {question:"¿Cómo se retira un documento de esta demo?",documentId:"control-documental"}
];
export function suggestionScope(suggestion, data) {
  if (!suggestions.includes(suggestion) ||
      (suggestion.documentId && !data.documents.some(d=>d.id===suggestion.documentId)))
    throw new Error("Sugerencia no disponible.");
  return suggestion.documentId;
}
export async function search(question, data, documentId="") {
  if (documentId && !data.documents.some(d=>d.id===documentId)) throw new Error("Documento no disponible.");
  await encodeQuery(question); // Preserve the bounded input contract.
  const query=[...new Set(searchTerms(question))];
  if (!query.length) throw new Error("Agrega una palabra específica del tema que buscas.");
  const rows=data.chunks.map(chunk=>{
    const doc=data.documents.find(d=>d.id===chunk.document_id);
    return {chunk,body:searchTerms(chunk.text),meta:searchTerms(doc.title+" "+chunk.section_title)};
  });
  const average=rows.reduce((n,r)=>n+r.body.length,0)/rows.length;
  // BM25 with k1=1.2, b=.75; metadata contributes a small, explicit boost.
  return rows.filter(r=>!documentId||r.chunk.document_id===documentId).map(r=>{
    let matched=0,score=0;
    for(const term of query) {
      const tf=r.body.filter(t=>t===term).length, metadata=r.meta.includes(term);
      if (!tf&&!metadata) continue;
      matched++;
      const df=rows.filter(x=>x.body.includes(term)||x.meta.includes(term)).length;
      const idf=Math.log(1+(rows.length-df+.5)/(df+.5));
      if(tf) score+=idf*(tf*2.2)/(tf+1.2*(.25+.75*r.body.length/average));
      if(metadata) score+=.25*idf;
    }
    return {chunk:r.chunk,score,matched};
  }).filter(r=>r.matched>=Math.min(query.length,Math.max(2,Math.ceil(query.length*.6)))&&r.score>0)
    .sort((a,b)=>b.score-a.score||a.chunk.id.localeCompare(b.chunk.id)).slice(0,3)
    .map(({chunk,score})=>({chunk,score}));
}
export async function resolveQuery(question,data,documentId="") {
  await encodeQuery(question);
  if (documentId&&!data.documents.some(d=>d.id===documentId)) throw new Error("Documento no disponible.");
  if(isCatalogQuery(question)) return {kind:"catalog",documents:data.documents};
  const hits=await search(question,data,documentId);
  if(hits.length) return {kind:"evidence",hits};
  return {kind:"no_match",hits:[],otherScopeAvailable:!!documentId&&(await search(question,data)).length>0};
}
export function createLimiter(now=()=>Date.now()) {
  let start=now(), used=0;
  return () => {
    if (now()-start>=60000) { start=now();used=0; }
    if (used>=30) throw new Error("Pausa un momento: máximo 30 consultas por minuto en esta pestaña.");
    used++;
  };
}
export async function readBounded(response, maxBytes) {
  if (!response.ok || !response.body) throw new Error("No se pudo cargar la demo.");
  const reader=response.body.getReader(); let size=0; const chunks=[];
  try {
    for (;;) {
      const {done,value}=await reader.read(); if (done) break;
      size+=value.length;
      if (size>maxBytes) throw new Error("El paquete supera el tamaño permitido.");
      chunks.push(value);
    }
  } catch (error) { await reader.cancel(); throw error; }
  const bytes=new Uint8Array(size); let offset=0;
  for (const chunk of chunks) { bytes.set(chunk,offset);offset+=chunk.length; }
  return bytes;
}
export async function loadBundle(fetcher=fetch) {
  const manifestBytes=await readBounded(await fetcher("./release.json",{cache:"no-store"}),16384);
  const manifest=JSON.parse(new TextDecoder().decode(manifestBytes));
  if (manifest.schema_version!==1 || manifest.engine!==ENGINE || manifest.retrieval_strategy!=="bm25-metadata-alias-v1" || manifest.policy_version!=="public-synthetic-only-v1" ||
      !/^[a-f0-9]{40}$/.test(manifest.source_commit) || typeof manifest.candidate_version!=="string" ||
      manifest.candidate_version.length>64 || !manifest.files?.["corpus.json"] ||
      !/^[a-f0-9]{64}$/.test(manifest.files["corpus.json"].sha256)) invalid();
  const bytes=await readBounded(await fetcher("./corpus.json",{cache:"no-store"}),1000000);
  const hash=[...new Uint8Array(await crypto.subtle.digest("SHA-256",bytes))].map(b=>b.toString(16).padStart(2,"0")).join("");
  if (hash!==manifest.files["corpus.json"].sha256 || bytes.length!==manifest.files["corpus.json"].bytes) invalid();
  const data=validateBundle(JSON.parse(new TextDecoder().decode(bytes)));
  if (data.corpus_version!==manifest.corpus_version) invalid();
  return {manifest,data};
}
