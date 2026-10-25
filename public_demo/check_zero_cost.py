"""Fail closed on the narrow CI configuration approved for zero provider spend."""
import re
from pathlib import Path
def validate(workflows):
    for name,text in workflows.items():
        runners=re.findall(r"^\s*runs-on:\s*(.+)$",text,re.M)
        if not runners or any(r.strip()!="ubuntu-latest" for r in runners):
            raise ValueError(f"{name}: only standard ubuntu-latest runners are approved")
        if text.count("if: github.event.repository.private == false")!=len(runners):
            raise ValueError(f"{name}: every job must stop if repository becomes private")
        if re.search(r"^\s*cache(?:-dependency-path)?:|upload-artifact|actions/cache|larger-runner",text,re.M):
            raise ValueError(f"{name}: caches, artifact uploads and paid runners are not approved")
        for action in re.findall(r"^\s*- uses:\s*([^ \n]+)",text,re.M):
            if not re.fullmatch(r"actions/(checkout|setup-python|setup-node)@[a-f0-9]{40}",action):
                raise ValueError(f"{name}: unapproved action")
    return len(workflows)
if __name__=="__main__":
    root=Path(__file__).resolve().parents[1]
    print({"zero_cost_workflows_checked":validate({p.name:p.read_text() for p in (root/".github/workflows").glob("*.yml")}),
           "scope":"static public repository / standard runner configuration; not an account billing audit"})
