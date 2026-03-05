"""
automate-prometheus-exporter

Prometheus metrics exporter for the automate-home project.
Listens to Redis for appliance state changes and pushes metrics to Prometheus Pushgateway.
"""

__version__ = "0.1.0"

from prometheus_exporter import conf

__all__ = ["__version__", "conf"]
