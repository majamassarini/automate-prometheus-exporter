import home
from prometheus_exporter.handler.appliance.curtain.outdoor import Handler as Parent


class Handler(Parent):
    """Handler for outdoor bedroom curtain."""

    KLASS = home.appliance.curtain.outdoor.bedroom.Appliance
    METRIC_PREFIX = "home_curtain_outdoor_bedroom"
