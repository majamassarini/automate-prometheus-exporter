import home
from prometheus_exporter.handler.appliance.handler import Handler as Parent


class Handler(Parent):
    """Handler for energy guard sockets."""

    KLASS = home.appliance.socket.energy_guard.Appliance
    METRIC_PREFIX = "home_socket_energy_guard"
    DESCRIPTION = "Socket state"

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
            == home.appliance.socket.energy_guard.state.on.State().VALUE
        ):
            return 1
        if (
            self._appliance.state.VALUE
            == home.appliance.socket.energy_guard.state.forced.on.State().VALUE
        ):
            return 2
        if (
            self._appliance.state.VALUE
            == home.appliance.socket.energy_guard.state.off.State().VALUE
        ):
            return 0
        if (
            self._appliance.state.VALUE
            == home.appliance.socket.energy_guard.state.forced.off.State().VALUE
        ):
            return -1
        return None
