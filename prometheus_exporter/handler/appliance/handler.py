from prometheus_exporter.handler.appliance.registry import Registry


class Handler(metaclass=Registry):
    """Base handler for appliance metrics."""

    KLASS = None  # Appliance class this handler applies to
    METRIC_PREFIX = "home"  # Prefix for metric names
    DESCRIPTION = "Home automation metric"

    def __init__(self, home_resources, appliance, exporter):
        self._home_resources = home_resources
        self._appliance = appliance
        self._exporter = exporter

    @property
    def metric_prefix(self):
        """Get the metric prefix (e.g., 'home_sensor_temperature')."""
        return self.METRIC_PREFIX

    @property
    def description(self):
        """Get the metric description."""
        return self.DESCRIPTION

    def get_metric_name(self):
        """Get the full metric name for this appliance."""
        return f"{self.metric_prefix}_value"

    def get_value(self):
        """
        Get the current value to export as a metric.

        :return: the appliance state VALUE, or None if not applicable
        """
        return self._appliance.state.VALUE
