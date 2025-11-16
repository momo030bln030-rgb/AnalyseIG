import sys
import runpy
from pathlib import Path

try:
    from tracing_setup import init_tracing
except Exception:
    init_tracing = None


def main():
    if len(sys.argv) < 2:
        print("Usage: python run_traced.py <script.py> [service_name] [otlp_endpoint]")
        sys.exit(1)

    script_path = Path(sys.argv[1])
    if not script_path.exists():
        print(f"Script not found: {script_path}")
        sys.exit(2)

    service_name = sys.argv[2] if len(sys.argv) > 2 else "ig_toolkit"
    otlp_endpoint = sys.argv[3] if len(sys.argv) > 3 else None

    if init_tracing:
        tracer = init_tracing(service_name=service_name, otlp_endpoint=otlp_endpoint)
    else:
        print("[tracing] tracing_setup nicht importierbar — Fortfahren ohne Tracing")
        class DummyTracer:
            def start_as_current_span(self, name):
                from contextlib import nullcontext
                return nullcontext()

        tracer = DummyTracer()

    with tracer.start_as_current_span(f"run:{script_path.name}"):
        print(f"[tracing] Running {script_path} (service={service_name})")
        # run the target script as __main__ so its if __name__ == '__main__' runs
        runpy.run_path(str(script_path), run_name="__main__")


if __name__ == "__main__":
    main()
