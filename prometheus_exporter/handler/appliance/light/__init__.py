import home
from prometheus_exporter.handler.appliance.handler import Handler as Parent


class Handler(Parent):
    """Handler for basic lights."""

    KLASS = home.appliance.light.Appliance
    METRIC_PREFIX = "home_light"
    DESCRIPTION = "Light state"

    def get_value(self):
        """
        Return numeric state value:
        0 = Off
        1 = On
        2 = Forced On
        -1 = Forced Off
        """
        if self._appliance.state.VALUE == home.appliance.light.state.on.State().VALUE:
            return 1
        if (
            self._appliance.state.VALUE
            == home.appliance.light.state.forced.on.State().VALUE
        ):
            return 2
        if self._appliance.state.VALUE == home.appliance.light.state.off.State().VALUE:
            return 0
        if (
            self._appliance.state.VALUE
            == home.appliance.light.state.forced.off.State().VALUE
        ):
            return -1
        return None


from prometheus_exporter.handler.appliance.light import indoor

__all__ = ["Handler", "indoor"]
