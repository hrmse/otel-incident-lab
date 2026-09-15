"""OpenTelemetry setup kept separate from request handling."""
from __future__ import annotations

import logging
import os

from opentelemetry import metrics, trace
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

RESOURCE = Resource.create({"service.name": "checkout-api", "service.version": "0.1.0"})


def configure_telemetry(app: object) -> metrics.Counter:
    """Attach exporters and create the application error counter."""
    endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "localhost:4317")
    tracer_provider = TracerProvider(resource=RESOURCE)
    export_enabled = os.getenv("OTEL_EXPORT_ENABLED", "true").lower() == "true"
    if export_enabled:
        tracer_provider.add_span_processor(
            BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint, insecure=True))
        )
    trace.set_tracer_provider(tracer_provider)

    readers = []
    if export_enabled:
        readers.append(PeriodicExportingMetricReader(OTLPMetricExporter(endpoint=endpoint, insecure=True)))
    meter_provider = MeterProvider(resource=RESOURCE, metric_readers=readers)
    metrics.set_meter_provider(meter_provider)
    FastAPIInstrumentor.instrument_app(app, tracer_provider=tracer_provider)

    logger = logging.getLogger("checkout-api")
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
    return meter_provider.get_meter("checkout-api").create_counter(
        "checkout_requests_total", description="Checkout requests grouped by outcome"
    )
