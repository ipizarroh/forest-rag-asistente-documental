import {readFile,writeFile,mkdir} from "node:fs/promises";
import {createHash} from "node:crypto";
import {search} from "./web/engine.mjs";
const raw=await readFile(new URL(process.argv[3]??"./acceptance-heldout.json",import.meta.url));
const bank=JSON.parse(raw),data=JSON.parse(await readFile("dist/public-demo/corpus.json"));
const results=[];
for(const c of bank.cases){const hits=await search(c.query,data);results.push({...c,top:hits[0]?{document:hits[0].chunk.document_id,section:hits[0].chunk.section}:null,passed:c.document?hits[0]?.chunk.document_id===c.document&&hits[0]?.chunk.section===c.section:hits.length===0});}
const report={bank_sha256:createHash("sha256").update(raw).digest("hex"),phase:process.argv[2]??"candidate",results,passed:results.filter(x=>x.passed).length,total:results.length};
await mkdir("reports/next001",{recursive:true});await writeFile("reports/next001/retrieval-"+report.phase+".json",JSON.stringify(report,null,2)+"\n");console.log(JSON.stringify(report));
