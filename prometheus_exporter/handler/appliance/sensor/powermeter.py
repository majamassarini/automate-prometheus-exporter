import home
from prometheus_exporter.handler.appliance.handler import Handler as Parent


class Handler(Parent):
    """Handler for power meter sensors."""

    KLASS = home.appliance.sensor.powermeter.Appliance
    METRIC_PREFIX = "home_sensor_power"
    DESCRIPTION = "Power in Watts"

    def get_value(self):
        """Power meters don't have a direct value, only events."""
        return None
