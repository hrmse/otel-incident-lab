"""Local incident-drill API. It has no persistence or real payment integration."""
from __future__ import annotations

import logging
import os

from fastapi import FastAPI, Header, HTTPException
from opentelemetry import trace

from checkout_api.telemetry import configure_telemetry

app = FastAPI(title="Checkout API Incident Lab")
REQUESTS = configure_telemetry(app)
LOGGER = logging.getLogger("checkout-api")
TRACER = trace.get_tracer("checkout-api")


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/checkout/{order_id}")
def checkout(order_id: str, x_debug_fail: str | None = Header(default=None)) -> dict[str, str]:
    """Return a synthetic checkout result or a deliberate lab-only 503."""
    with TRACER.start_as_current_span("checkout.process") as span:
        span.set_attribute("checkout.order_id", order_id)
        span.set_attribute("checkout.synthetic", True)
        failure_enabled = os.getenv("LAB_ALLOW_DEBUG_FAILURES", "false").lower() == "true"
        if x_debug_fail == "true" and failure_enabled:
            span.set_attribute("checkout.outcome", "error")
            REQUESTS.add(1, {"outcome": "error"})
            LOGGER.error("synthetic checkout failure order_id=%s", order_id)
            raise HTTPException(status_code=503, detail="synthetic lab failure")
        span.set_attribute("checkout.outcome", "success")
        REQUESTS.add(1, {"outcome": "success"})
        LOGGER.info("synthetic checkout success order_id=%s", order_id)
        return {"order_id": order_id, "status": "accepted"}
