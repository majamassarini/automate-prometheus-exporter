import home
from prometheus_exporter.handler.appliance.curtain.outdoor import Handler as Parent


class Handler(Parent):
    """Handler for outdoor bedroom curtain."""

    KLASS = home.appliance.curtain.outdoor.bedroom.Appliance
    METRIC_PREFIX = "home_curtain_outdoor_bedroom"

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
            == home.appliance.curtain.outdoor.bedroom.state.opened.State.VALUE
        ):
            return 0
        if (
            self._appliance.state.VALUE
            == home.appliance.curtain.outdoor.bedroom.state.forced.opened.State.VALUE
        ):
            return -1
        if (
            self._appliance.state.VALUE
            == home.appliance.curtain.outdoor.bedroom.state.closed.State.VALUE
        ):
            return 1
        if (
            self._appliance.state.VALUE
            == home.appliance.curtain.outdoor.bedroom.state.forced.closed.State.VALUE
        ):
            return 2
        return None
