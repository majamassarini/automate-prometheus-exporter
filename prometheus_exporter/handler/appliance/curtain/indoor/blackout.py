import home
from prometheus_exporter.handler.appliance.curtain.outdoor import Handler as Parent


class Handler(Parent):
    """Handler for indoor blackout curtain."""

    KLASS = home.appliance.curtain.indoor.blackout.Appliance

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
            == home.appliance.curtain.indoor.blackout.state.opened.State.VALUE
        ):
            return 0
        if (
            self._appliance.state.VALUE
            == home.appliance.curtain.indoor.blackout.state.forced.opened.State.VALUE
        ):
            return -1
        if (
            self._appliance.state.VALUE
            == home.appliance.curtain.indoor.blackout.state.closed.State.VALUE
        ):
            return 1
        if (
            self._appliance.state.VALUE
            == home.appliance.curtain.indoor.blackout.state.forced.closed.State.VALUE
        ):
            return 2
        return None
