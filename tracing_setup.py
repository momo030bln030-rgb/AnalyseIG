from contextlib import nullcontext

def _safe_import(name, package=None):
    try:
        module = __import__(name)
        return module
    except Exception:
        return None

try:
    from opentelemetry import trace
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter
    # OTLP exporter (optional)
    try:
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
    except Exception:
        OTLPSpanExporter = None
except Exception:
    trace = None
    TracerProvider = None
    Resource = None
    SimpleSpanProcessor = None
    ConsoleSpanExporter = None
    OTLPSpanExporter = None


def init_tracing(service_name: str = "ig_toolkit", otlp_endpoint: str | None = None):
    """Initialisiert einen einfachen OpenTelemetry-Tracer.

    - Schreibt Spans auf die Konsole mittels `ConsoleSpanExporter`.
    - Optional: Wenn `otlp_endpoint` angegeben und der OTLP-Exporter installiert ist,
      wird ein OTLP Exporter hinzugefügt.

    Rückgabe: ein Tracer-Objekt (oder ein Dummy-Tracer bei Fehlern).
    """
    if trace is None:
        # OpenTelemetry nicht installiert — Dummy-Tracer
        class DummyTracer:
            def start_as_current_span(self, name):
                return nullcontext()

        print("[tracing] opentelemetry nicht installiert — Dummy-Tracer wird verwendet")
        return DummyTracer()

    try:
        resource = Resource.create({"service.name": service_name})
        provider = TracerProvider(resource=resource)
        trace.set_tracer_provider(provider)

        # Optionaler OTLP Exporter
        if otlp_endpoint and OTLPSpanExporter is not None:
            try:
                exporter = OTLPSpanExporter(endpoint=otlp_endpoint)
                provider.add_span_processor(SimpleSpanProcessor(exporter))
                print(f"[tracing] OTLP Exporter verbunden: {otlp_endpoint}")
            except Exception as e:
                print(f"[tracing] OTLP Exporter Fehler: {e}")

        # Console Exporter für lokale Sichtbarkeit
        provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))
        tracer = trace.get_tracer(service_name)
        print(f"[tracing] Tracer initialisiert für Service: {service_name}")
        return tracer
    except Exception as e:
        print(f"[tracing] Initialisierung fehlgeschlagen: {e}")

        class DummyTracer:
            def start_as_current_span(self, name):
                return nullcontext()

        return DummyTracer()
