#!/usr/bin/env python3

import sys
import asyncio
import importlib
import inspect
import logging.config
import pkgutil

import home
import prometheus_exporter.conf
from prometheus_client import CollectorRegistry, Enum, Gauge, push_to_gateway


sys.path.append("..")


class OnRedisMsg(home.builder.listener.OnRedisMsg):
    def __init__(
        self,
        home_resources,
        pushgateway_host,
        pushgateway_port,
        job_name="automate_home",
    ):
        self._home_resources = home_resources
        self._pushgateway_host = pushgateway_host
        self._pushgateway_port = pushgateway_port
        self._job_name = job_name
        self._logger = logging.getLogger(__name__)

        self._registry = CollectorRegistry()
        self._enums = {}
        self._gauges = {}
        self._state_values_cache = {}

    @staticmethod
    def _metric_prefix(appliance):
        """Derive a Prometheus metric prefix from the appliance class module path.

        Strips the leading ``home.appliance.`` components and joins the rest
        with underscores, prefixed with ``home_``.

        Example: ``home.appliance.light.indoor.dimmerable``
        → ``home_light_indoor_dimmerable``
        """
        parts = appliance.__class__.__module__.split(".")
        return "home_" + "_".join(parts[2:])  # skip "home" and "appliance"

    def _discover_state_values(self, appliance_class):
        """Return a sorted list of state VALUE strings for *appliance_class*.

        Walks the ``<module>.state`` subpackage recursively, collects every
        ``VALUE`` class attribute that is a non-empty string (and not the
        default ``"None"``), and caches the result per appliance class.
        """
        if appliance_class in self._state_values_cache:
            return self._state_values_cache[appliance_class]

        state_pkg_name = f"{appliance_class.__module__}.state"
        values = set()

        try:
            state_pkg = importlib.import_module(state_pkg_name)
        except ImportError:
            self._state_values_cache[appliance_class] = []
            return []

        if not hasattr(state_pkg, "__path__"):
            self._state_values_cache[appliance_class] = []
            return []

        for _finder, submod_name, _ispkg in pkgutil.walk_packages(
            state_pkg.__path__, prefix=f"{state_pkg_name}."
        ):
            try:
                submod = importlib.import_module(submod_name)
                for _name, obj in inspect.getmembers(
                    submod, inspect.isclass
                ):
                    if not obj.__module__.startswith(state_pkg_name):
                        continue
                    val = getattr(obj, "VALUE", None)
                    if isinstance(val, str) and val not in ("None", ""):
                        values.add(val)
            except Exception:
                pass

        result = sorted(values)
        self._state_values_cache[appliance_class] = result
        return result

    def _get_or_create_enum(self, metric_name, description, states):
        """Get or create an Enum metric for the given *states*."""
        if metric_name not in self._enums:
            self._enums[metric_name] = Enum(
                metric_name,
                description,
                labelnames=["appliance"],
                states=states,
                registry=self._registry,
            )
        return self._enums[metric_name]

    def _get_or_create_gauge(self, metric_name, description):
        """Get or create a Gauge metric."""
        if metric_name not in self._gauges:
            self._gauges[metric_name] = Gauge(
                metric_name,
                description,
                labelnames=["appliance"],
                registry=self._registry,
            )
        return self._gauges[metric_name]

    def push_to_pushgateway(self):
        """Push all metrics to the Prometheus Pushgateway."""
        try:
            gateway_url = (
                f"{self._pushgateway_host}:{self._pushgateway_port}"
            )
            push_to_gateway(
                gateway_url,
                job=self._job_name,
                registry=self._registry,
            )
            self._logger.debug(
                f"Pushed metrics to Pushgateway at {gateway_url}"
            )
        except Exception as e:
            self._logger.error(f"Failed to push to Pushgateway: {e}")

    async def on_appliance_updated(self, new_appliance):
        appliance = self._home_resources.appliances.find(new_appliance.name)
        old_state, new_state = appliance.update(new_appliance)

        prefix = self._metric_prefix(appliance)

        # Export current state as an Enum metric when the appliance has
        # meaningful named states (non-sensor appliances).
        state_values = self._discover_state_values(appliance.__class__)
        if state_values:
            current_value = appliance.state.VALUE
            if current_value in state_values:
                enum_metric = self._get_or_create_enum(
                    f"{prefix}_state",
                    f"{appliance.__class__.__name__} state",
                    states=state_values,
                )
                enum_metric.labels(appliance=appliance.name).state(
                    current_value
                )
                self._logger.info(
                    f"Updated {prefix}_state"
                    f'{{appliance="{appliance.name}"}} = {current_value}'
                )

        # Export numeric measurements from float/int events (sensor appliances).
        for event in new_state - old_state:
            if isinstance(event, float):
                metric_name = f"{prefix}_float_value"
                gauge = self._get_or_create_gauge(
                    metric_name,
                    f"{appliance.__class__.__name__} measurement",
                )
                gauge.labels(appliance=appliance.name).set(float(event))
                self._logger.info(
                    f"Updated {metric_name}"
                    f'{{appliance="{appliance.name}"}} = {event}'
                )
            elif isinstance(event, int) and not isinstance(event, bool):
                metric_name = f"{prefix}_int_value"
                gauge = self._get_or_create_gauge(
                    metric_name,
                    f"{appliance.__class__.__name__} measurement",
                )
                gauge.labels(appliance=appliance.name).set(int(event))
                self._logger.info(
                    f"Updated {metric_name}"
                    f'{{appliance="{appliance.name}"}} = {event}'
                )

        await asyncio.get_running_loop().run_in_executor(
            None, self.push_to_pushgateway
        )

    async def on_performer_updated(self, performer, old_state, new_state):
        self._logger.debug(f"{old_state} {new_state}")
        performer.execute(old_state, new_state)


if __name__ == "__main__":
    (options, _) = home.options.parser().parse_args()
    if options.configuration_file:
        options = home.configs.parse(vars(options), options.configuration_file)

    # Import plugins based on configuration
    if options.knx_usbhid or options.knxnet_ip:
        import knx_plugin
    if options.lifx:
        import lifx_plugin
    if options.sonos:
        import soco_plugin
    if options.somfy_sdn:
        import somfy_sdn_plugin
    if options.home_assistant:
        import home_assistant_plugin

    configuration = prometheus_exporter.conf.default_logging_configuration(
        options.logging_dir,
        logging_level=options.prometheus_exporter_logging_level,
    )
    logging.config.dictConfig(configuration)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    resources = home.builder.listener.Resources(
        options.project_dir,
        options.redis_host,
        options.redis_port,
        options.prometheus_exporter_node_name,
        options.prometheus_exporter_other_nodes_names,
    )

    on_redis_msg = OnRedisMsg(
        resources,
        options.prometheus_exporter_pushgateway_host,
        options.prometheus_exporter_pushgateway_port,
        options.prometheus_exporter_job_name,
    )

    loop.run_until_complete(resources.redis_gateway.connect())
    resources.redis_gateway.create_tasks(
        loop,
        on_redis_msg.on_appliance_updated,
        on_redis_msg.on_performer_updated,
    )
    loop.run_forever()
