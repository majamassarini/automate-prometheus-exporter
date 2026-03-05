import home
from prometheus_exporter.handler.appliance.handler import Handler as Parent


class Handler(Parent):
    """Handler for presence thermostats."""

    KLASS = home.appliance.thermostat.presence.Appliance
    METRIC_PREFIX = "home_thermostat_presence"
    DESCRIPTION = "Thermostat state"
