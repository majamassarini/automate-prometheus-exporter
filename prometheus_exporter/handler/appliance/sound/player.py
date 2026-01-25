import home
from prometheus_exporter.handler.appliance.handler import Handler as Parent


class Handler(Parent):
    """Handler for sound player appliances."""

    KLASS = home.appliance.sound.player.Appliance
    METRIC_PREFIX = "home_sound_player"
    DESCRIPTION = "Sound player state"

    def get_value(self):
        """
        Return numeric state value:
        0 = Off
        1 = Fade In
        2 = Fade Out
        3 = Forced On
        4 = Forced Circadian Rhythm
        5 = Forced Off
        """
        if (
            self._appliance.state.VALUE
            == home.appliance.sound.player.state.off.State().VALUE
        ):
            return 0
        if (
            self._appliance.state.VALUE
            == home.appliance.sound.player.state.fade_in.State().VALUE
        ):
            return 1
        if (
            self._appliance.state.VALUE
            == home.appliance.sound.player.state.fade_out.State().VALUE
        ):
            return 2
        if (
            self._appliance.state.VALUE
            == home.appliance.sound.player.state.forced.on.State().VALUE
        ):
            return 3
        if (
            self._appliance.state.VALUE
            == home.appliance.sound.player.state.forced.circadian_rhythm.State().VALUE
        ):
            return 4
        if (
            self._appliance.state.VALUE
            == home.appliance.sound.player.state.forced.off.State().VALUE
        ):
            return 5
        return None
