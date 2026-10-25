"""Helpers for driving tools/sp.py from Python (sp-promo-a production, 2026-10-24).

compile_script(dict, path) writes a screenplay and compiles it (new filenames only);
route(...) and simulate(...) return parsed JSON results. All commands go through sp.py,
so they use the snapshot engine jar and the three verified ROMs.
"""
import json
import subprocess
import sys
from pathlib import Path

SP = Path(__file__).resolve().parent / 'sp.py'


def run(args, cwd=None):
    proc = subprocess.run([sys.executable, str(SP), *map(str, args)], cwd=cwd,
                          capture_output=True, text=True)
    try:
        result = json.loads(proc.stdout.strip().splitlines()[-1]) if proc.stdout.strip() else {}
    except json.JSONDecodeError:
        result = {'ok': False, 'error': proc.stdout[-2000:]}
    result['_exit'] = proc.returncode
    result['_stderr_tail'] = proc.stderr[-1500:]
    return result


def compile_script(script, path):
    path = Path(path)
    script_path = path.with_suffix('.screenplay.json') if path.suffix == '.stageplay' else path
    scene_path = script_path.with_name(script_path.name.replace('.screenplay.json', '.stageplay'))
    for p in (script_path, scene_path):
        if p.exists():
            p.unlink()   # probe files only; production takes use fresh names
    script_path.write_text(json.dumps(script, indent=1))
    result = run(['compile', '--script', script_path.name, '--out', scene_path.name], cwd=script_path.parent)
    if not result.get('ok'):
        raise RuntimeError(f"compile failed: {result.get('error')}")
    return scene_path


def route(scene, actor, frame, x, y, out, extra=(), cwd=None):
    out = Path(out)
    if out.exists():
        out.unlink()
    return run(['route', '--scene', scene, '--actor', actor, '--frame', frame, '--x', x, '--y', y,
                '--out', out, *extra], cwd=cwd)


def simulate(scene, out, every=1):
    out = Path(out)
    if out.exists():
        out.unlink()
    result = run(['simulate', '--scene', scene, '--out', out, '--every', every])
    if not result.get('ok'):
        raise RuntimeError(f"simulate failed: {result.get('error')}")
    return [json.loads(line) for line in out.read_text().splitlines()]
