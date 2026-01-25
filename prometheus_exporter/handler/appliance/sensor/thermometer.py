import home
from prometheus_exporter.handler.appliance.handler import Handler as Parent


class Handler(Parent):
    """Handler for thermometer sensors."""

    KLASS = home.appliance.sensor.thermometer.Appliance
    METRIC_PREFIX = "home_sensor_temperature"
    DESCRIPTION = "Temperature in degrees Celsius"

    def get_value(self):
        """Temperature sensors don't have a direct value, only events."""
        return None
