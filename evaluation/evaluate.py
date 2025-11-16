import subprocess
import sys
import time
import json
from pathlib import Path
from typing import List, Dict, Any


def now_ts():
    return time.time()


def run_command(cmd: List[str], cwd: Path = Path('.')) -> Dict[str, Any]:
    start = now_ts()
    try:
        proc = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, timeout=600)
        rc = proc.returncode
        out = proc.stdout
        err = proc.stderr
    except Exception as e:
        rc = -1
        out = ''
        err = repr(e)
    end = now_ts()
    return {"rc": rc, "stdout": out, "stderr": err, "start": start, "end": end, "duration": end - start}


def find_recent_reports(start_ts: float, report_dir: Path) -> List[Path]:
    candidates = []
    for p in report_dir.glob("*_REPORT.json"):
        try:
            if p.stat().st_mtime >= start_ts:
                candidates.append(p)
        except Exception:
            continue
    for p in report_dir.glob("*_FULL_REPORT.json"):
        try:
            if p.stat().st_mtime >= start_ts and p not in candidates:
                candidates.append(p)
        except Exception:
            continue
    return candidates


def parse_report(path: Path) -> Dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return {"valid": False}

    summary = {"valid": True}
    # heuristics: count posts, comments, likes if present
    if isinstance(data, dict):
        posts = data.get('posts') or data.get('results') or []
        summary['posts_count'] = len(posts) if isinstance(posts, list) else 0
        # try to sum comments
        total_comments = 0
        for p in posts:
            if isinstance(p, dict):
                c = p.get('comments')
                if isinstance(c, list):
                    total_comments += len(c)
        summary['comments_count'] = total_comments
        # follower-like fields
        profile = data.get('profile') or {}
        summary['follower_count'] = profile.get('follower_count') or profile.get('followers') or None
    else:
        summary.update({"posts_count": 0, "comments_count": 0})
    return summary


def evaluate(config: Dict[str, Any]):
    workspace = Path(config.get('workspace', '.'))
    report_dir = Path(config.get('report_dir', workspace))
    runs = []

    targets = config.get('targets', [])
    iterations = int(config.get('iterations', 1))

    for t in targets:
        script = t.get('script')
        args = t.get('args', [])
        label = t.get('label') or script
        runs.append({'label': label, 'script': script, 'args': args})

    results = []

    for r in runs:
        for i in range(iterations):
            print(f"[eval] Running {r['label']} (iter {i+1}/{iterations})")
            start_ts = now_ts()
            cmd = [sys.executable, 'run_traced.py', r['script']] + r['args']
            out = run_command(cmd, cwd=workspace)
            found_reports = find_recent_reports(start_ts - 1.0, report_dir)
            parsed = [parse_report(p) for p in found_reports]
            results.append({
                'label': r['label'],
                'iteration': i + 1,
                'cmd': cmd,
                'rc': out['rc'],
                'duration': out['duration'],
                'stdout': out['stdout'][:2000],
                'stderr': out['stderr'][:2000],
                'reports': [str(p) for p in found_reports],
                'parsed_reports': parsed,
            })

    summary = {'runs': results}
    out_path = report_dir / f'evaluation_report_{int(time.time())}.json'
    out_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"[eval] Evaluation complete. Report: {out_path}")


def main():
    cfg = Path('evaluation/config_sample.json')
    if len(sys.argv) > 1:
        cfg = Path(sys.argv[1])
    if not cfg.exists():
        print(f"Config not found: {cfg}")
        sys.exit(2)
    config = json.loads(cfg.read_text(encoding='utf-8'))
    evaluate(config)


if __name__ == '__main__':
    main()
