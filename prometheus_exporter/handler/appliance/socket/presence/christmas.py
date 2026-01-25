import home
from prometheus_exporter.handler.appliance.socket.energy_guard import Handler as Parent


class Handler(Parent):
    """Handler for Christmas presence socket."""

    KLASS = home.appliance.socket.presence.christmas.Appliance

    def get_value(self):
        """
        Return numeric state value:
        0 = Off
        1 = On
        2 = Forced On
        -1 = Forced Off
        """
        if (
            self._appliance.state.VALUE
            == home.appliance.socket.presence.christmas.state.on.State().VALUE
        ):
            return 1
        if (
            self._appliance.state.VALUE
            == home.appliance.socket.presence.christmas.state.forced.on.State().VALUE
        ):
            return 2
        if (
            self._appliance.state.VALUE
            == home.appliance.socket.presence.christmas.state.off.State().VALUE
        ):
            return 0
        if (
            self._appliance.state.VALUE
            == home.appliance.socket.presence.christmas.state.forced.off.State().VALUE
        ):
            return -1
        return None
