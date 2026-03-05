import home
from prometheus_exporter.handler.appliance.light import Handler as Parent


class Handler(Parent):
    """Handler for zone lights."""

    KLASS = home.appliance.light.zone.Appliance
    METRIC_PREFIX = "home_light_indoor_zone"
