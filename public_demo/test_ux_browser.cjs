const {chromium}=require("playwright");
const assert=require("node:assert/strict"),fs=require("node:fs/promises");
const base=process.env.FORESTRAG_UX_URL||"http://127.0.0.1:8768/";
(async()=>{
 const browser=await chromium.launch({headless:true,...(process.env.FORESTRAG_BROWSER_EXECUTABLE?{executablePath:process.env.FORESTRAG_BROWSER_EXECUTABLE}:{})});
 const checks=[];
 for(const viewport of [{width:1440,height:1080},{width:390,height:844}]) {
  const ctx=await browser.newContext({viewport,isMobile:viewport.width===390});
  const page=await ctx.newPage(),errors=[],requests=[];
  page.on("pageerror",e=>errors.push(e.message));page.on("request",r=>requests.push(r.url()));
  await page.goto(base,{waitUntil:"networkidle"});await page.waitForFunction(()=>!document.getElementById("submit").disabled);
  const ask=async q=>{await page.locator("#question").fill(q);await page.locator("#submit").click();await page.waitForFunction(()=>!document.getElementById("submit").disabled);};
  await page.locator("#document").selectOption("registro-terreno");
  await ask("¿Qué puedo encontrar en ForestRAG?");
  assert.equal(await page.locator(".catalog-entry").count(),3);
  assert.equal(await page.locator("#document").inputValue(),"registro-terreno");
  assert.match(await page.locator("#scope-notice").innerText(),/conserva tu filtro/);
  checks.push({id:"UX-01/02",viewport:viewport.width,status:"PASS"});
  await page.getByRole("button",{name:"¿Cómo se retira un documento de esta demo?",exact:true}).click();
  await page.waitForFunction(()=>!document.getElementById("submit").disabled);
  assert.equal(await page.locator("#document").inputValue(),"control-documental");
  assert.match(await page.locator("#scope-notice").innerText(),/Ámbito de la sugerencia/);
  assert.match(await page.locator(".result").first().innerText(),/siguiente construcción/);
  await page.locator(".result a").first().click();
  assert.equal(await page.locator("#source-control-documental").getAttribute("open"),"");
  checks.push({id:"UX-05/06",viewport:viewport.width,status:"PASS"});
  await page.locator("#document").selectOption("registro-terreno");
  await ask("¿Cómo se retira un documento de esta demo?");
  assert.equal(await page.locator(".result").count(),0);
  assert.equal(await page.locator("#document").inputValue(),"registro-terreno");
  await page.getByRole("button",{name:"Buscar esta consulta en todos los documentos públicos"}).click();
  await page.waitForFunction(()=>!document.getElementById("submit").disabled);
  assert.equal(await page.locator("#document").inputValue(),"");
  assert.ok(await page.locator(".result").count()>0);
  checks.push({id:"UX-06-explicit-expansion",viewport:viewport.width,status:"PASS"});
  for(const [q,expected] of [
   ["¿Qué campos registra una observación?","fecha, sector, responsable"],
   ["¿Qué se revisa antes de comparar imágenes?","resolución espacial"],
   ["¿Qué datos hay que anotar en terreno?","hallazgo"]]) {
    await ask(q);assert.ok((await page.locator(".result").first().innerText()).includes(expected));
  }
  checks.push({id:"UX-03/04/08",viewport:viewport.width,status:"PASS"});
  await ask("¿Cuál es la contraseña de mi correo?");
  assert.equal(await page.locator(".result").count(),0);assert.match(await page.locator("#status").innerText(),/No encontré evidencia/);
  const before=requests.length;
  await ask('<img src=x onerror="window.xssExecuted=true">');
  assert.equal(await page.evaluate(()=>window.xssExecuted),undefined);
  assert.equal(requests.length,before);
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
  assert.deepEqual(errors,[]);
  checks.push({id:"UX-07/09-mobile-layout",viewport:viewport.width,status:"PASS"});
  await ctx.close();
 }
 const ctx=await browser.newContext(),page=await ctx.newPage();
 await page.route("**/corpus.json",r=>r.fulfill({status:200,contentType:"application/json",body:'{"tampered":true}'}));
 await page.goto(base,{waitUntil:"networkidle"});
 await page.waitForFunction(()=>document.getElementById("status").textContent.includes("No se pudo verificar"));
 assert.equal(await page.locator("#submit").isDisabled(),true);
 checks.push({id:"UX-10",status:"PASS"});
 await ctx.close();await browser.close();
 const report={base,checks,status:"PASS"};
 await fs.mkdir("reports/next001",{recursive:true});
 await fs.writeFile(process.env.FORESTRAG_UX_RESULT||"reports/next001/browser-ux.json",JSON.stringify(report,null,2)+"\n");
 console.log(JSON.stringify(report));
})().catch(e=>{console.error(e);process.exitCode=1;});
