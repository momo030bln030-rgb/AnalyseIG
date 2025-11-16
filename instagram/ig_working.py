"""Wrapper: starts root `ig_working.py` from `instagram/` folder with optional tracing."""
import runpy
from pathlib import Path
from tracing_helper import span_context

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / 'ig_working.py'

if __name__ == '__main__':
    with span_context('instagram:ig_working'):
        runpy.run_path(str(TARGET), run_name='__main__')
