import home
from prometheus_exporter.handler.appliance.light import Handler as Parent


class Handler(Parent):
    """Handler for zone lights."""

    KLASS = home.appliance.light.zone.Appliance

    def get_value(self):
        """
        Return numeric state value:
        0 = Off
        1 = On
        2 = Alarmed On
        3 = Alarmed Off
        4 = Forced On
        5 = Forced Off
        """
        if (
            self._appliance.state.VALUE
            == home.appliance.light.zone.state.off.State().VALUE
        ):
            return 0
        if (
            self._appliance.state.VALUE
            == home.appliance.light.zone.state.on.State().VALUE
        ):
            return 1
        if (
            self._appliance.state.VALUE
            == home.appliance.light.zone.state.alarmed.on.State().VALUE
        ):
            return 2
        if (
            self._appliance.state.VALUE
            == home.appliance.light.zone.state.alarmed.off.State().VALUE
        ):
            return 3
        if (
            self._appliance.state.VALUE
            == home.appliance.light.zone.state.forced.on.State().VALUE
        ):
            return 4
        if (
            self._appliance.state.VALUE
            == home.appliance.light.zone.state.forced.off.State().VALUE
        ):
            return 5
        return None
