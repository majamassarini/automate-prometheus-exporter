import home
from prometheus_exporter.handler.appliance.light import Handler as Parent


class Handler(Parent):
    """Handler for dimmerable lights."""

    KLASS = home.appliance.light.indoor.dimmerable.Appliance

    def get_value(self):
        """
        Return numeric state value:
        0 = Off
        1 = On
        2 = Forced On
        3 = Forced Lux Balance
        4 = Forced Circadian Rhythm
        5 = Forced Show
        """
        if (
            self._appliance.state.VALUE
            == home.appliance.light.indoor.dimmerable.state.off.State().VALUE
        ):
            return 0
        if (
            self._appliance.state.VALUE
            == home.appliance.light.indoor.dimmerable.state.on.State().VALUE
        ):
            return 1
        if (
            self._appliance.state.VALUE
            == home.appliance.light.indoor.dimmerable.state.forced.on.State().VALUE
        ):
            return 2
        if (
            self._appliance.state.VALUE
            == home.appliance.light.indoor.dimmerable.state.forced.lux_balance.State().VALUE
        ):
            return 3
        if (
            self._appliance.state.VALUE
            == home.appliance.light.indoor.dimmerable.state.forced.circadian_rhythm.State().VALUE
        ):
            return 4
        if (
            self._appliance.state.VALUE
            == home.appliance.light.indoor.dimmerable.state.forced.show.State().VALUE
        ):
            return 5
        return None
