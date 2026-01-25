from prometheus_exporter.handler.event.handler import Handler as Parent


class Handler(Parent):
    """Handler for float event values."""

    KLASS = float
    METRIC_SUFFIX = "float_value"
    DESCRIPTION = "Float value from event"

    def get_value(self):
        """Return the float value directly."""
        return float(self._event)
