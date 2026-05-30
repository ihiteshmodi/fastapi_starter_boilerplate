from unittest import mock

import pytest
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
from tenacity import wait_none


@pytest.fixture(scope="session", autouse=True)
def clean_tracer_provider():
    """Initialize once and shutdown once to avoid noisy background-thread teardown errors."""
    exporter = InMemorySpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)

    yield

    provider.shutdown()


@pytest.fixture(autouse=True)
def remove_retry_waits():
    """Patch retry waits to zero so tests stay fast and deterministic."""
    with mock.patch(
        "app.common.utils_authentication.AuthenticationService.call_authentication_service.retry.wait",
        wait_none(),
    ):
        yield


def test_retry_path_without_sleep(client):
    response = client.get("/healthz")
    assert response.status_code == 200
