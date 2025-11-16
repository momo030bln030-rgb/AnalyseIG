"""Wrapper: startet das Root-`facebook_analyzer.py` aus dem obersten Verzeichnis mit optionalem Tracing."""
import runpy
from pathlib import Path
from tracing_helper import span_context

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / 'facebook_analyzer.py'

if __name__ == '__main__':
    with span_context('facebook:facebook_analyzer'):
        runpy.run_path(str(TARGET), run_name='__main__')
