from pathlib import Path
import argparse,difflib
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--base',default='revisao_interface_2026_10_25/originais');p.add_argument('--output',required=True);p.add_argument('files',nargs='+');args=p.parse_args()
chunks=[]
for name in args.files:
    original=ROOT/args.base/name
    if not original.exists():original=ROOT/args.base/Path(name).name
    current=ROOT/name
    before=original.read_text(encoding='utf-8').splitlines(keepends=True) if original.exists() else []
    after=current.read_text(encoding='utf-8').splitlines(keepends=True) if current.exists() else []
    chunks.extend(difflib.unified_diff(before,after,fromfile='baseline/'+name,tofile=name,n=8))
target=ROOT/args.output;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(''.join(chunks),encoding='utf-8')
print(str(target),len(chunks),'diff lines')
