"""Wrapper: starts root `ig_full_scraper.py` from `instagram/` folder with tracing."""
import runpy
from pathlib import Path
from tracing_helper import span_context

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / 'ig_full_scraper.py'

if __name__ == '__main__':
    with span_context('instagram:ig_full_scraper'):
        runpy.run_path(str(TARGET), run_name='__main__')
