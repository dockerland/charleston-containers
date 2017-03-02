# Overview

## Prometheus

Prometheus, a [Cloud Native Computing Foundation](https://cncf.io/) project, is a systems and service monitoring system. It collects metrics
from configured targets at given intervals, evaluates rule expressions,
displays the results, and can trigger alerts if some condition is observed
to be true.

### Highlights

- Consumes up to 800,000 metrics per second on a single server
- Static Go Binary
- Support both pull and push methods
- Large number of clients (cAdvisor, node-exporter, experimental docker support in 1.13)
- Supports advanced rule evaluation such as linear predictions and quantile analysis

### Caveats

- No down-sampling support
- No official long-term storage support (two week default)
- No clustering (must run multiple instances for redundancy)
- Must run separate alert manager (or depend on Grafana)

### Pull versus Push

- Both are scalable
- Adopt the model that makes sense in your environment
- Personally prefer pull, no reconfiguring of clients to deploy a new instance

## Grafana

Creates beautiful charts from time series databases, including Prometheus and other.

### Highlights

- Prefered Prometheus visualization tool
- Built-in alerting as of 4.0
- Query syntax is identical to Prometheus
- Canned dashboards for cAdvisor, node-exporter, Redis etc available on their website

## cAdvisor

- Container exporter from Google
- Native Prometheus support at /metrics
- Provides network, storage, CPU and memory metrics per container for Prometheus
- Canned dashboard available for Grafana

## Custom Endpoints

- Build /metrics endpoints directly into your application
- Expose metrics on latency, number of calls and other metrics directly to Prometheus

