#!/usr/bin/env python3

import sys
import asyncio
import logging.config
import time

import home
import prometheus_exporter.conf
import prometheus_exporter.handler.appliance.registry
import prometheus_exporter.handler.event.registry
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway


sys.path.append("..")


class OnRedisMsg(home.builder.listener.OnRedisMsg):
    def __init__(self, home_resources, pushgateway_host, pushgateway_port, job_name="automate_home"):
        self._home_resources = home_resources
        self._pushgateway_host = pushgateway_host
        self._pushgateway_port = pushgateway_port
        self._job_name = job_name
        self._logger = logging.getLogger(__name__)

        # Registry for metrics
        self._registry = CollectorRegistry()

        # Metric caches - store Gauge objects by metric name
        self._gauges = {}

    def get_or_create_gauge(self, metric_name, description, labels=None):
        """Get or create a Gauge metric."""
        if metric_name not in self._gauges:
            if labels:
                self._gauges[metric_name] = Gauge(
                    metric_name,
                    description,
                    labelnames=labels,
                    registry=self._registry
                )
            else:
                self._gauges[metric_name] = Gauge(
                    metric_name,
                    description,
                    registry=self._registry
                )
        return self._gauges[metric_name]

    def push_to_pushgateway(self):
        """Push all metrics to Pushgateway."""
        try:
            gateway_url = f"{self._pushgateway_host}:{self._pushgateway_port}"
            push_to_gateway(
                gateway_url,
                job=self._job_name,
                registry=self._registry
            )
            self._logger.debug(f"Pushed metrics to Pushgateway at {gateway_url}")
        except Exception as e:
            self._logger.error(f"Failed to push to Pushgateway: {e}")

    async def on_appliance_updated(self, new_appliance):
        appliance_handler = None
        event_handler = None

        appliance = self._home_resources.appliances.find(new_appliance.name)
        old_state, new_state = appliance.update(new_appliance)

        try:
            appliance_handler = prometheus_exporter.handler.appliance.registry[
                appliance.__class__
            ]
            appliance_handler = appliance_handler(self._home_resources, appliance, self)
        except KeyError:
            self._logger.debug(f"Appliance {appliance} not mapped")

        # Process events from state changes
        for event in new_state - old_state:
            try:
                event_handler = prometheus_exporter.handler.event.registry[
                    event.__class__
                ]
                event_handler = event_handler(self._home_resources, event, self)
            except KeyError:
                self._logger.debug(f"Event {event} not mapped")

            if appliance_handler and event_handler:
                # Get metric name and value from handlers
                metric_name = f"{appliance_handler.metric_prefix}_{event_handler.metric_suffix}"
                metric_name = metric_name.replace(".", "_").replace("-", "_")
                value = event_handler.get_value()

                if value is not None:
                    gauge = self.get_or_create_gauge(
                        metric_name,
                        f"{appliance_handler.description} - {event_handler.description}",
                        labels=["appliance"]
                    )
                    gauge.labels(appliance=appliance.name).set(value)
                    self._logger.info(f"Updated metric {metric_name}{{appliance=\"{appliance.name}\"}} = {value}")

        # Process appliance-level metrics
        if appliance_handler:
            value = appliance_handler.get_value()
            if value is not None:
                metric_name = appliance_handler.get_metric_name()
                metric_name = metric_name.replace(".", "_").replace("-", "_")

                gauge = self.get_or_create_gauge(
                    metric_name,
                    appliance_handler.description,
                    labels=["appliance"]
                )
                gauge.labels(appliance=appliance.name).set(value)
                self._logger.info(f"Updated metric {metric_name}{{appliance=\"{appliance.name}\"}} = {value}")

        # Push all metrics to Pushgateway
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
        options.logging_dir, logging_level=options.prometheus_exporter_logging_level
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
        loop, on_redis_msg.on_appliance_updated, on_redis_msg.on_performer_updated
    )
    loop.run_forever()
