import home
from prometheus_exporter.handler.appliance.handler import Handler as Parent


class Handler(Parent):
    """Handler for basic lights."""

    KLASS = home.appliance.light.Appliance
    METRIC_PREFIX = "home_light"
    DESCRIPTION = "Light state"

from prometheus_exporter.handler.appliance.light import indoor

__all__ = ["Handler", "indoor"]
