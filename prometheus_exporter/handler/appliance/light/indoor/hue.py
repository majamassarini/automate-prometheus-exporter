import home
from prometheus_exporter.handler.appliance.light.indoor.dimmerable import Handler as Parent


class Handler(Parent):
    """Handler for Hue lights."""

    KLASS = home.appliance.light.indoor.hue.Appliance
    METRIC_PREFIX = "home_light_indoor_hue"
