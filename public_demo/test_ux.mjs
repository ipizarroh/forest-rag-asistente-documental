import test from "node:test";
import assert from "node:assert/strict";
import {readFile} from "node:fs/promises";
import {resolveQuery,search,suggestions,suggestionScope,isCatalogQuery} from "./web/engine.mjs";
const data=JSON.parse(await readFile("dist/public-demo/corpus.json"));
for(const question of [
 "¿Qué puedo encontrar en ForestRAG?","¿Qué puedo consultar?","¿Qué información tiene ForestRAG?",
 "¿Qué documentos hay disponibles?","¿De qué trata esta aplicación?","¿Qué información puedo encontrar aquí?",
 "¿Qué temas puedo explorar?","¿Qué documentos puedo consultar?"]) {
 test("catalog: "+question,async()=>{
  const result=await resolveQuery(question,data,"registro-terreno");
  assert.equal(result.kind,"catalog");assert.deepEqual(result.documents,data.documents);
 });
}
for(const [id,q,doc,section] of [
 ["UX-03","¿Qué campos registra una observación?","registro-terreno",1],
 ["UX-04","¿Qué se revisa antes de comparar imágenes?","monitoreo-forestal",2],
 ["UX-05","¿Cómo se retira un documento de esta demo?","control-documental",2],
 ["UX-08","¿Qué datos hay que anotar en terreno?","registro-terreno",1]
])test(id,async()=>{
 const result=await resolveQuery(q,data);assert.equal(result.kind,"evidence");
 assert.equal(result.hits[0].chunk.document_id,doc);assert.equal(result.hits[0].chunk.section,section);
 assert.equal(isCatalogQuery(q),false);
});
test("UX-06: suggestion scope is explicit and bound to available public docs",()=>{
 for(const suggestion of suggestions)assert.equal(suggestionScope(suggestion,data),suggestion.documentId);
 assert.throws(()=>suggestionScope({question:"fake",documentId:"private"},data));
});
test("manual scope stays constrained; expansion offered only on public evidence",async()=>{
 const r=await resolveQuery("¿Cómo se retira un documento de esta demo?",data,"registro-terreno");
 assert.equal(r.kind,"no_match");assert.equal(r.otherScopeAvailable,true);
});
test("UX-07: absent information abstains, with no claim about hidden documents",async()=>{
 const r=await resolveQuery("¿Cuál es la clave secreta del correo?",data);
 assert.equal(r.kind,"no_match");assert.equal(r.otherScopeAvailable,false);
});
test("UX-09: special characters and prompt text cannot expand public scope",async()=>{
 for(const q of ["<script>alert(1)</script>","🔥 ¿Qué CAMPOS registra una observación?","'; DROP TABLE documents; --"]) {
  const r=await resolveQuery(q,data);
  assert.ok(["evidence","no_match"].includes(r.kind));
  if(r.hits)assert.ok(r.hits.every(h=>data.documents.some(d=>d.id===h.chunk.document_id)));
 }
});
test("catalog route obeys bounded inputs and rejects unknown scope",async()=>{
 await assert.rejects(resolveQuery("Qué puedo consultar ".repeat(100),data));
 await assert.rejects(resolveQuery("¿Qué documentos hay?",data,"private"));
});
