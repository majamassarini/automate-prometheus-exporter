import home
from prometheus_exporter.handler.appliance.handler import Handler as Parent


class Handler(Parent):
    """Handler for presence thermostats."""

    KLASS = home.appliance.thermostat.presence.Appliance
    METRIC_PREFIX = "home_thermostat_presence"
    DESCRIPTION = "Thermostat state"

    def get_value(self):
        """
        Return numeric state value:
        0 = Off
        1 = Keep
        2 = Forced Keep
        3 = On
        4 = Forced On
        -1 = Forced Off
        """
        if (
            self._appliance.state.VALUE
            == home.appliance.thermostat.presence.state.keep.State().VALUE
        ):
            return 1
        if (
            self._appliance.state.VALUE
            == home.appliance.thermostat.presence.state.forced.keep.State().VALUE
        ):
            return 2
        if (
            self._appliance.state.VALUE
            == home.appliance.thermostat.presence.state.on.State().VALUE
        ):
            return 3
        if (
            self._appliance.state.VALUE
            == home.appliance.thermostat.presence.state.forced.on.State().VALUE
        ):
            return 4
        if (
            self._appliance.state.VALUE
            == home.appliance.thermostat.presence.state.off.State().VALUE
        ):
            return 0
        if (
            self._appliance.state.VALUE
            == home.appliance.thermostat.presence.state.forced.off.State().VALUE
        ):
            return -1
        return None
