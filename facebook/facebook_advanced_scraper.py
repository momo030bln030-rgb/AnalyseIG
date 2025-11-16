"""Wrapper: starts the root `facebook_advanced_scraper.py` from the project root with tracing."""
import runpy
from pathlib import Path
from tracing_helper import span_context

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / 'facebook_advanced_scraper.py'

if __name__ == '__main__':
    with span_context('facebook:facebook_advanced_scraper'):
        runpy.run_path(str(TARGET), run_name='__main__')
