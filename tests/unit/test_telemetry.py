import os
import threading
import time

import pytest

import nexla_sdk.telemetry as telemetry


class _FakeNoOpProvider:
    pass


class _FakeProvider:
    pass


class _FakeTracer:
    def __init__(self):
        self.started = []

    # Context manager API compatibility for spans
    def start_as_current_span(self, *args, **kwargs):
        self.started.append((args, kwargs))
        return _FakeSpan()

    def start_span(self, *args, **kwargs):
        self.started.append((args, kwargs))
        return _FakeSpan()


class _FakeSpan:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def is_recording(self):
        return False

    def set_attribute(self, *_, **__):
        pass

    def set_status(self, *_, **__):
        pass

    def record_exception(self, *_, **__):
        pass


class _FakeTraceModule:
    def __init__(self):
        # Start with a NoOp-like provider
        self._provider = self.NoOpTracerProvider()
        self._get_tracer_calls = 0
        self._lock = threading.Lock()

    class NoOpTracerProvider:  # noqa: D401 - shape compat only
        pass

    def get_tracer_provider(self):
        return self._provider

    def set_provider_non_noop(self):
        self._provider = _FakeProvider()

    def get_tracer(self, *_args, **_kwargs):
        with self._lock:
            self._get_tracer_calls += 1
        return _FakeTracer()


@pytest.fixture(autouse=True)
def restore_env_and_state(monkeypatch):
    # Snapshot env vars we may touch
    original_env = dict(os.environ)
    # Snapshot telemetry internals we may tweak
    original_avail = telemetry._opentelemetry_available
    original_trace = getattr(telemetry, "trace", None)
    original_tracer = getattr(telemetry, "_tracer", None)

    yield

    # Restore env
    os.environ.clear()
    os.environ.update(original_env)
    # Restore telemetry internals
    telemetry._opentelemetry_available = original_avail
    telemetry.trace = original_trace
    telemetry._tracer = original_tracer


def test_is_tracing_configured_false_when_otel_missing(monkeypatch):
    monkeypatch.setattr(telemetry, "_opentelemetry_available", False, raising=False)
    assert telemetry.is_tracing_configured() is False


def test_get_tracer_returns_noop_when_disabled_or_missing(monkeypatch):
    # Disabled explicitly
    t = telemetry.get_tracer(False)
    assert hasattr(t, "start_as_current_span")

    # Enabled but OTEL unavailable
    monkeypatch.setattr(telemetry, "_opentelemetry_available", False, raising=False)
    t2 = telemetry.get_tracer(True)
    assert hasattr(t2, "start_as_current_span")


def test_is_tracing_configured_detects_non_noop_provider(monkeypatch):
    fake_trace = _FakeTraceModule()
    monkeypatch.setattr(telemetry, "_opentelemetry_available", True, raising=False)
    monkeypatch.setattr(telemetry, "trace", fake_trace, raising=False)

    # NoOp provider -> False
    assert telemetry.is_tracing_configured() is False

    # Non-noop provider -> True
    fake_trace.set_provider_non_noop()
    assert telemetry.is_tracing_configured() is True


def test_is_tracing_configured_env_heuristics(monkeypatch):
    fake_trace = _FakeTraceModule()
    monkeypatch.setattr(telemetry, "_opentelemetry_available", True, raising=False)
    monkeypatch.setattr(telemetry, "trace", fake_trace, raising=False)

    # Keep provider noop, rely on env
    for var in [
        "OTEL_EXPORTER_OTLP_ENDPOINT",
        "OTEL_EXPORTER_OTLP_TRACES_ENDPOINT",
        "OTEL_EXPORTER_JAEGER_AGENT_HOST",
        "OTEL_EXPORTER_ZIPKIN_ENDPOINT",
        "OTEL_SERVICE_NAME",
    ]:
        os.environ[var] = "x"
        assert telemetry.is_tracing_configured() is True
        del os.environ[var]


def test_get_tracer_caches_single_instance_thread_safe(monkeypatch):
    fake_trace = _FakeTraceModule()
    monkeypatch.setattr(telemetry, "_opentelemetry_available", True, raising=False)
    monkeypatch.setattr(telemetry, "trace", fake_trace, raising=False)
    monkeypatch.setattr(telemetry, "_tracer", None, raising=False)

    # Create concurrent callers to amplify race potential
    start = threading.Barrier(10)
    done = []

    def _call_get_tracer():
        start.wait()
        # Trigger a small delay to widen init window
        time.sleep(0.01)
        t = telemetry.get_tracer(True)
        assert hasattr(t, "start_as_current_span")
        done.append(t)

    threads = [threading.Thread(target=_call_get_tracer) for _ in range(10)]
    for th in threads:
        th.start()
    for th in threads:
        th.join()

    # Ensure only one underlying get_tracer call occurred
    assert fake_trace._get_tracer_calls == 1
    # And all callers received the same tracer instance
    first = done[0]
    assert all(id(t) == id(first) for t in done)
