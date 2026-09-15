# Local incident drill runbook

## Trigger

Start the Compose stack, confirm the health endpoint, then send one request with
the X-Debug-Fail header. This switch is enabled only by the local Compose
environment; never copy it to a deployment pipeline.

## Triage

1. Confirm the synthetic error counter changed in Prometheus.
2. Find the request trace in Tempo by the synthetic order ID.
3. Compare span status, service attributes and the correlated Loki log.
4. Record only verified observations. This lab cannot establish root cause for a
   real system.

## Recovery

Stop issuing failure requests. The API has no state, no downstream integration
and no remediation action. Use docker compose down to end the local drill.
