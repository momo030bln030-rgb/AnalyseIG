"""Lightweight tracing helper used by wrappers.

Provides `get_tracer()` and `span_context(name)` which work even if
OpenTelemetry is not installed (fall back to nullcontext).
"""
from contextlib import nullcontext
import os

try:
    from tracing_setup import init_tracing
except Exception:
    init_tracing = None


def get_tracer(service_name: str = None):
    service = service_name or os.environ.get('TRACING_SERVICE', 'ig_toolkit')
    if init_tracing:
        return init_tracing(service_name=service)
    # dummy tracer
    class DummyTracer:
        def start_as_current_span(self, name):
            return nullcontext()

    return DummyTracer()


def span_context(name: str, service_name: str = None):
    tracer = get_tracer(service_name=service_name)
    return tracer.start_as_current_span(name)
