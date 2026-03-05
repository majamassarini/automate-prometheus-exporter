import home
from prometheus_exporter.handler.appliance.curtain.outdoor import Handler as Parent


class Handler(Parent):
    """Handler for indoor blackout curtain."""

    KLASS = home.appliance.curtain.indoor.blackout.Appliance
    METRIC_PREFIX = "home_curtain_indoor_blackout"
