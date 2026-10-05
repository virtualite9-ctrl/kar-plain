"""Native Hermes security scan of the content-only port; no forced install."""
from pathlib import Path
import dataclasses,json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
code="""import dataclasses,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
from tools.skills_guard import scan_skill,should_allow_install
root=Path(sys.argv[1]);result=scan_skill(root,source='community');allow,reason=should_allow_install(result,force=False)
output={'verdict':result.verdict,'allow':allow,'reason':reason,'findings':[dataclasses.asdict(x) for x in result.findings]}
print(json.dumps(output,ensure_ascii=False))
raise SystemExit(0 if allow is True else 2)
"""
cmd=json.loads(subprocess.check_output(['hermes','--print-runtime-command'],text=True))
native=cmd[0]
boot="import sys;sys.dont_write_bytecode=True;sys.path.insert(0,sys.argv.pop(1));import hermes_bootstrap;exec(sys.argv.pop(1))"
result=subprocess.run([native,'-I','-c',boot,str(Path.home()/'.hermes/hermes-agent'),code,str(ROOT/'hermes/kar-plain')],capture_output=True,text=True,timeout=60)
print(result.stdout,end='')
if result.stderr:print(result.stderr,file=sys.stderr,end='')
raise SystemExit(result.returncode)
