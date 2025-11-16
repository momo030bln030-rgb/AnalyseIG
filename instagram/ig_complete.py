"""Wrapper: startet das Root-`ig_complete.py` aus dem obersten Verzeichnis.
Dieser Wrapper initialisiert optional Tracing und startet das Target unter einem Span.
"""
import runpy
from pathlib import Path
from tracing_helper import span_context

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / 'ig_complete.py'

if __name__ == '__main__':
    with span_context('instagram:ig_complete'):
        runpy.run_path(str(TARGET), run_name='__main__')
