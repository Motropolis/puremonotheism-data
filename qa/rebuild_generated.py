#!/usr/bin/env python3
import subprocess,sys,os
R=os.path.abspath(sys.argv[1] if len(sys.argv)>1 and not sys.argv[1].startswith('--') else '.'); CHECK='--check' in sys.argv
names=['rebuild_roots.py','rebuild_meta_roots_index.py','rebuild_interlinear.py','rebuild_browse.py','rebuild_search.py','rebuild_suggest.py']; fail=0
for name in names:
 args=[sys.executable,os.path.join(R,'qa',name),R]+(['--check'] if CHECK else []); r=subprocess.run(args,capture_output=True,text=True)
 print(f"[{'PASS' if r.returncode==0 else 'FAIL'}] {name}: {(r.stdout+r.stderr).strip()}"); fail += r.returncode!=0
print(f'generated rebuild gate: builders={len(names)} failures={fail}'); sys.exit(1 if fail else 0)
