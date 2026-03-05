import home
from prometheus_exporter.handler.appliance.handler import Handler as Parent


class Handler(Parent):
    """Handler for energy guard sockets."""

    KLASS = home.appliance.socket.energy_guard.Appliance
    METRIC_PREFIX = "home_socket_energy_guard"
    DESCRIPTION = "Socket state"
