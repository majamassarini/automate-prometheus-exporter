import home
from prometheus_exporter.handler.appliance.light import Handler as Parent


class Handler(Parent):
    """Handler for presence lights."""

    KLASS = home.appliance.light.presence.Appliance
    METRIC_PREFIX = "home_light_indoor_presence"
