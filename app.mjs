import {loadBundle,resolveQuery,createLimiter,suggestions,suggestionScope} from "./engine.mjs";
const $=id=>document.getElementById(id);
function element(tag,text,className) {
  const el=document.createElement(tag); if (text!==undefined) el.textContent=text;
  if (className) el.className=className; return el;
}
const limit=createLimiter();
try {
  const {manifest,data}=await loadBundle();
  const byId=new Map(data.documents.map(d=>[d.id,d]));
  function sourceLink(docId,text) {
    const link=element("a",text);link.href="#source-"+docId;
    link.addEventListener("click",()=>{$("source-"+docId).open=true;});return link;
  }
  for (const doc of data.documents) {
    const option=element("option",doc.title);option.value=doc.id;$("document").append(option);
    const details=element("details");details.id="source-"+doc.id;
    details.append(element("summary",doc.title),element("p","SINTÉTICO · PÚBLICO · v"+doc.version,"source-meta"));
    for(const section of doc.sections) details.append(element("h3",section.title),element("p",section.text));
    $("sources").append(details);
  }
  $("version").textContent=manifest.candidate_version+" · "+manifest.source_commit.slice(0,7)+(manifest.source_dirty?" · copia de trabajo":"");
  $("status").textContent="Listo: "+data.documents.length+" documentos ficticios. Pregunta qué puedes consultar o elige un tema.";
  for(const id of ["question","document","submit"]) $(id).disabled=false;
  let busy=false;
  const scopeNotice=$("scope-notice");
  for(const suggestion of suggestions) {
    const button=element("button",suggestion.question);button.type="button";
    button.addEventListener("click",()=>{
      if(busy) return;
      const next=suggestionScope(suggestion,data),changed=$("document").value!==next;
      $("document").value=next;$("question").value=suggestion.question;
      scopeNotice.textContent=changed
        ? "Ámbito de la sugerencia: "+(next?byId.get(next).title:"todos los documentos públicos")+"."
        : "La sugerencia usa "+(next?byId.get(next).title:"todos los documentos públicos")+".";
      $("search-form").requestSubmit();
    });$("suggestions").append(button);
  }
  $("document").addEventListener("change",()=>{
    scopeNotice.textContent="Filtro elegido: "+($("document").value?byId.get($("document").value).title:"todos los documentos públicos")+".";
  });
  $("search-form").addEventListener("submit",async event=>{
    event.preventDefault();if(busy) return;
    $("status").classList.remove("error");
    try {
      limit();busy=true;$("submit").disabled=true;$("results").setAttribute("aria-busy","true");
      $("status").textContent="Buscando en los documentos verificados…";
      const response=await resolveQuery($("question").value,data,$("document").value);
      $("results").replaceChildren();
      if(response.kind==="catalog") {
        $("status").textContent="Catálogo público: "+response.documents.length+" documentos ficticios. Puedes buscar fragmentos y revisar sus fuentes. No hay generación con IA.";
        if($("document").value) scopeNotice.textContent="La orientación muestra todo el catálogo público. Se conserva tu filtro para las búsquedas documentales.";
        for(const doc of response.documents) {
          const article=element("article",undefined,"catalog-entry");
          article.append(element("h3",doc.title),element("p",doc.sections.map(s=>s.title).join(" · ")),sourceLink(doc.id,"Explorar documento público"));
          $("results").append(article);
        }
      } else if(response.kind==="evidence") {
        $("status").textContent=response.hits.length+" fragmentos encontrados mediante búsqueda léxica BM25. Revisa la fuente antes de concluir.";
        for(const {chunk} of response.hits) {
          const article=element("article",undefined,"result");article.dataset.chunkId=chunk.id;
          article.append(element("h3",byId.get(chunk.document_id).title),element("blockquote",chunk.text),
            sourceLink(chunk.document_id,"Ver fuente · sección "+chunk.section+": "+chunk.section_title));
          $("results").append(article);
        }
      } else {
        $("status").textContent="No encontré evidencia suficiente con estas palabras en el ámbito elegido. La búsqueda léxica puede omitir otras formas de preguntar; no demuestra que la información no exista.";
        const help=element("p","Prueba palabras del tema, revisa los documentos disponibles o pregunta «¿Qué puedo consultar?». No puedo confirmar datos ausentes ni información privada.");
        $("results").append(help);
        if(response.otherScopeAvailable) {
          const expand=element("button","Buscar esta consulta en todos los documentos públicos");expand.type="button";
          expand.addEventListener("click",()=>{
            $("document").value="";scopeNotice.textContent="Ampliaste explícitamente la búsqueda a todos los documentos públicos.";
            $("search-form").requestSubmit();
          });$("results").append(expand);
        }
      }
    } catch(error) {
      $("results").replaceChildren();$("status").textContent=error.message;$("status").classList.add("error");
    } finally {
      busy=false;$("submit").disabled=false;$("results").setAttribute("aria-busy","false");
    }
  });
} catch {
  $("status").textContent="No se pudo verificar el corpus. Recarga la página o revisa el repositorio.";
  $("status").classList.add("error");$("results").replaceChildren();
}
