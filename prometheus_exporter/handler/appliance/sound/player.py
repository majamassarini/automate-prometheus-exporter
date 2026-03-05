import home
from prometheus_exporter.handler.appliance.handler import Handler as Parent


class Handler(Parent):
    """Handler for sound player appliances."""

    KLASS = home.appliance.sound.player.Appliance
    METRIC_PREFIX = "home_sound_player"
    DESCRIPTION = "Sound player state"
