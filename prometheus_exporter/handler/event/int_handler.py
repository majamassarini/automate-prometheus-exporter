from prometheus_exporter.handler.event.handler import Handler as Parent


class Handler(Parent):
    """Handler for integer event values."""

    KLASS = int
    METRIC_SUFFIX = "int_value"
    DESCRIPTION = "Integer value from event"

    def get_value(self):
        """Return the integer value directly."""
        return int(self._event)
