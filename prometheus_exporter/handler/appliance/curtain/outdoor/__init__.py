import home
from prometheus_exporter.handler.appliance.handler import Handler as Parent


class Handler(Parent):
    """Handler for outdoor curtains."""

    KLASS = home.appliance.curtain.outdoor.Appliance
    METRIC_PREFIX = "home_curtain_outdoor"
    DESCRIPTION = "Curtain state"

from prometheus_exporter.handler.appliance.curtain.outdoor import bedroom

__all__ = ["Handler", "bedroom"]
