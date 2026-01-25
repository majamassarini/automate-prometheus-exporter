import home
from prometheus_exporter.handler.appliance.handler import Handler as Parent


class Handler(Parent):
    """Handler for outdoor curtains."""

    KLASS = home.appliance.curtain.outdoor.Appliance
    METRIC_PREFIX = "home_curtain_outdoor"
    DESCRIPTION = "Curtain state"

    def get_value(self):
        """
        Return numeric state value:
        0 = Opened
        -1 = Forced Opened
        1 = Closed
        2 = Forced Closed
        """
        if (
            self._appliance.state.VALUE
            == home.appliance.curtain.outdoor.state.opened.State.VALUE
        ):
            return 0
        if (
            self._appliance.state.VALUE
            == home.appliance.curtain.outdoor.state.forced.opened.State.VALUE
        ):
            return -1
        if (
            self._appliance.state.VALUE
            == home.appliance.curtain.outdoor.state.closed.State.VALUE
        ):
            return 1
        if (
            self._appliance.state.VALUE
            == home.appliance.curtain.outdoor.state.forced.closed.State.VALUE
        ):
            return 2
        return None


from prometheus_exporter.handler.appliance.curtain.outdoor import bedroom

__all__ = ["Handler", "bedroom"]
