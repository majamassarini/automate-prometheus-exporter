from prometheus_exporter.handler.appliance.handler import Handler
from prometheus_exporter.handler.appliance.registry import registry

# Import all appliance handlers
from prometheus_exporter.handler.appliance import sensor

__all__ = ["Handler", "registry", "sensor"]
