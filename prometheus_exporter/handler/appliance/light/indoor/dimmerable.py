import home
from prometheus_exporter.handler.appliance.light import Handler as Parent


class Handler(Parent):
    """Handler for dimmerable lights."""

    KLASS = home.appliance.light.indoor.dimmerable.Appliance
    METRIC_PREFIX = "home_light_indoor_dimmerable"
