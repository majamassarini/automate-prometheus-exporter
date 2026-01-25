from prometheus_exporter.handler.event.registry import Registry


class Handler(metaclass=Registry):
    """Base handler for event metrics."""

    KLASS = None  # Event class this handler applies to
    METRIC_SUFFIX = "value"  # Suffix for metric names
    DESCRIPTION = "Event value"

    def __init__(self, home_resources, event, exporter):
        self._home_resources = home_resources
        self._event = event
        self._exporter = exporter

    @property
    def metric_suffix(self):
        """Get the metric suffix."""
        return self.METRIC_SUFFIX

    @property
    def description(self):
        """Get the event description."""
        return self.DESCRIPTION

    def get_value(self):
        """
        Get the numeric value from the event.
        Override in subclasses for specific event types.

        :return: numeric value or None
        """
        return None
