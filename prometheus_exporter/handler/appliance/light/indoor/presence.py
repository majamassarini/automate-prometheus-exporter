import home
from prometheus_exporter.handler.appliance.light import Handler as Parent


class Handler(Parent):
    """Handler for presence lights."""

    KLASS = home.appliance.light.presence.Appliance
    METRIC_PREFIX = "home_light_indoor_presence"

    def get_value(self):
        """
        Return numeric state value:
        0 = Off
        1 = Forced On
        """
        if (
            self._appliance.state.VALUE
            == home.appliance.light.presence.state.off.State().VALUE
        ):
            return 0
        if (
            self._appliance.state.VALUE
            == home.appliance.light.presence.state.forced.on.State().VALUE
        ):
            return 1
        return None
