# OpenTelemetry Incident Lab

A deliberately small checkout API and local observability platform for practising
an SRE investigation across metrics, traces and logs. It is a reproducible lab,
not a claim of production traffic, availability or incident outcomes.

## What it demonstrates

- OpenTelemetry SDK instrumentation for HTTP spans and application metrics.
- An OpenTelemetry Collector with bounded batching that routes signals to Tempo,
  Prometheus and Loki.
- Grafana datasource provisioning and an investigation dashboard starter.
- A safe local failure switch that produces a 503 and a correlated signal.
- Non-root containers, read-only application filesystem, dropped Linux
  capabilities and a minimal CI validation path.

## Architecture

    Drill client --> Checkout API --> OpenTelemetry Collector --> Tempo
                                                     |--> Prometheus
                                                     '--> Loki
    Grafana queries Tempo, Prometheus and Loki

## Run a local drill

    docker compose up --build
    curl -i http://localhost:8080/healthz
    curl -i -H 'X-Debug-Fail: true' http://localhost:8080/checkout/demo-order

Open Grafana at http://localhost:3000 and use the Checkout incident
investigation dashboard. The debug header is local-lab-only; the service
refuses it unless LAB_ALLOW_DEBUG_FAILURES=true.

## Investigation flow

1. In Prometheus, query checkout_requests_total grouped by outcome.
2. In Grafana Explore, locate the request trace in Tempo using
   checkout.order_id=demo-order.
3. In Loki, filter by service_name=checkout-api and pivot with trace context.
4. Record verified evidence and follow
   [the drill runbook](docs/incident-runbook.md).

## Repository map

- src: application and telemetry setup.
- deploy: Compose, Collector, Tempo, Prometheus, Loki and Grafana config.
- docs: threat model and incident drill runbook.
- tests: API and configuration boundary tests.

## Security and operational boundaries

No credentials are committed. The lab uses anonymous local Grafana access only;
do not expose it beyond localhost. Production deployments should pin images by
digest, use TLS/mTLS for OTLP, authenticate Grafana, enforce tenant boundaries,
scrub sensitive attributes and set retention/access policies outside this
repository. See [the threat model](docs/threat-model.md).

## Validate

    python -m pip install -e '.[dev]'
    ruff check src tests
    pytest
    docker compose config
