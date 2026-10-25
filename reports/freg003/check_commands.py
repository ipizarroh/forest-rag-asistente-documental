from pathlib import Path
import json, os, socket, subprocess, sys, time
from importlib.metadata import distributions
root=Path(__file__).resolve().parents[2]
py=str(root/".venv/Scripts/python.exe")
report=root/"reports/freg003"
report.mkdir(parents=True,exist_ok=True)
commands=[]
def run(args, label, timeout=40):
    p=subprocess.run([py,*args],cwd=root,capture_output=True,text=True,encoding="utf-8",errors="replace",timeout=timeout,env={**os.environ,"PYTHONIOENCODING":"utf-8"})
    row={"id":label,"command":["python",*args],"exit_code":p.returncode,"stdout":p.stdout,"stderr":p.stderr}
    commands.append(row)
    print(label, p.returncode, p.stdout.strip()[:350])
    return p
try:
    assert run(["-m","pip","check"],"CMD01").returncode==0
    p=run(["-m","forestrag.cli","demo"],"CMD02")
    assert p.returncode==0
    result=json.loads(p.stdout)
    assert result.get("passages") and not result.get("abstained")
    assert run(["-m","forestrag.security_http","init"],"CMD03").returncode==0
    server=subprocess.Popen([py,"-m","forestrag.security_http","serve"],cwd=root,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,creationflags=subprocess.CREATE_NO_WINDOW)
    try:
        for attempt in range(50):
            try:
                with socket.create_connection(("127.0.0.1",8510),timeout=.2): break
            except OSError:
                if server.poll() is not None: raise RuntimeError("Lab server exited")
                time.sleep(.1)
        else: raise RuntimeError("Lab readiness timeout")
        p=run(["scripts/demo_security.py"],"CMD04")
        assert p.returncode==0 and p.stdout.count("PASS")==6
    finally:
        server.terminate()
        try: server.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server.kill();server.wait(timeout=5)
    p=run(["-m","pytest","-q","tests/test_security_lab.py","tests/test_index_trust.py","--basetemp=data/pytest-doc-repro","--junitxml=reports/freg003/windows-security.xml"],"CMD05",60)
    assert p.returncode==0
finally:
    (report/"commands.json").write_text(json.dumps({"platform":sys.platform,"python":sys.version,"commands":commands},indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
