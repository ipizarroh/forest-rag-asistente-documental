import {loadBundle,search,createLimiter} from "./engine.mjs";
const $=id=>document.getElementById(id);
function element(tag,text,className) {
  const el=document.createElement(tag); if (text!==undefined) el.textContent=text;
  if (className) el.className=className; return el;
}
const suggestions=["¿Qué campos registra una observación de terreno?","¿Qué se revisa antes de comparar imágenes?","¿Cómo se retira un documento de esta demo?"];
const limit=createLimiter();
try {
  const {manifest,data}=await loadBundle();
  const byId=new Map(data.documents.map(d=>[d.id,d]));
  for (const doc of data.documents) {
    const option=element("option",doc.title);option.value=doc.id;$("document").append(option);
    const details=element("details");details.id="source-"+doc.id;
    details.append(element("summary",doc.title),element("p","SINTÉTICO · PÚBLICO · v"+doc.version,"source-meta"));
    for (const section of doc.sections) details.append(element("h3",section.title),element("p",section.text));
    $("sources").append(details);
  }
  $("version").textContent=manifest.candidate_version+" · "+manifest.source_commit.slice(0,7)+(manifest.source_dirty?" · copia de trabajo":"");
  $("status").textContent="Listo: "+data.documents.length+" documentos ficticios. Elige una consulta.";
  for (const id of ["question","document","submit"]) $(id).disabled=false;
  for (const question of suggestions) {
    const button=element("button",question);button.type="button";
    button.addEventListener("click",()=>{ $("question").value=question;$("search-form").requestSubmit(); });
    $("suggestions").append(button);
  }
  let busy=false;
  $("search-form").addEventListener("submit",async event=>{
    event.preventDefault();if (busy) return;
    $("status").classList.remove("error");
    try {
      limit();busy=true;$("submit").disabled=true;
      const hits=await search($("question").value,data,$("document").value);
      $("results").replaceChildren();
      $("status").textContent=hits.length ? hits.length+" fragmentos encontrados. Revisa la fuente antes de concluir."
        : "No encontré evidencia suficiente con estas palabras. Prueba otra consulta o revisa los documentos.";
      for (const {chunk} of hits) {
        const article=element("article",undefined,"result");article.dataset.chunkId=chunk.id;
        article.append(element("h3",byId.get(chunk.document_id).title),
          element("blockquote",chunk.text));
        const link=element("a","Ver fuente · sección "+chunk.section+": "+chunk.section_title);
        link.href="#source-"+chunk.document_id;
        link.addEventListener("click",()=>{ $("source-"+chunk.document_id).open=true; });
        article.append(link);$("results").append(article);
      }
    } catch (error) { $("results").replaceChildren();$("status").textContent=error.message;$("status").classList.add("error"); }
    finally {busy=false;$("submit").disabled=false;}
  });
} catch {
  $("status").textContent="No se pudo verificar el corpus. Recarga la página o revisa el repositorio.";
  $("status").classList.add("error");$("results").replaceChildren();
}
