import home
from prometheus_exporter.handler.appliance.handler import Handler as Parent


class Handler(Parent):
    """Handler for lux meter (light) sensors."""

    KLASS = home.appliance.sensor.luxmeter.Appliance
    METRIC_PREFIX = "home_sensor_lux"
    DESCRIPTION = "Light intensity in lux"

    def get_value(self):
        """Lux meters don't have a direct value, only events."""
        return None
