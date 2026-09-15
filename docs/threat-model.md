# Threat model

Telemetry can contain sensitive data. The lab only emits a synthetic order ID;
it must not receive names, addresses, payment data, session tokens or raw
request bodies. In a real environment apply attribute allow-lists, TLS/mTLS,
authentication, tenant separation, encryption, retention controls and access
auditing. Grafana anonymous mode is local-only and binds to loopback in Compose.
