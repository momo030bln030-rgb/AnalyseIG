"""Wrapper: starts root `ig.py` for convenience under `instagram/` folder.
Optional tracing span is created around the execution.
"""
import runpy
from pathlib import Path
from tracing_helper import span_context

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / 'ig.py'

if __name__ == '__main__':
    with span_context('instagram:ig'):
        runpy.run_path(str(TARGET), run_name='__main__')
