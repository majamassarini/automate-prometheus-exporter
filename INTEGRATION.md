# Integration with automate-home

This document describes how automate-prometheus-exporter integrates with the automate-home ecosystem.

## Overview

The prometheus-exporter acts as a bridge between the automate-home state machine system and Prometheus monitoring.

```
┌──────────────────────────────────────────────────────────────────────┐
│                        AUTOMATE-HOME ECOSYSTEM                        │
└──────────────────────────────────────────────────────────────────────┘

┌─────────────┐      ┌─────────┐      ┌────────────────────┐
│ KNX Plugin  │─────▶│         │      │  prometheus-       │
├─────────────┤      │         │      │  exporter          │
│Sonos Plugin │─────▶│  Redis  │─────▶│                    │
├─────────────┤      │ PubSub  │      │ - Listens to Redis │
│Lifx Plugin  │─────▶│         │      │ - Maps events      │
├─────────────┤      │         │      │ - Pushes metrics   │
│ HA Plugin   │─────▶│         │      │                    │
└─────────────┘      └─────────┘      └──────────┬─────────┘
      ▲                                           │
      │                                           ▼
┌─────┴──────┐                            ┌──────────────┐
│ automate-  │                            │ Pushgateway  │
│   home     │                            │              │
│  (brain)   │                            └──────┬───────┘
│            │                                   │
│ - State    │                                   ▼
│   machines │                            ┌─────────────┐
│ - Events   │                            │ Prometheus  │
│ - Commands │                            │             │
└────────────┘                            └──────┬──────┘
                                                 │
                                                 ▼
                                          ┌─────────────┐
                                          │   Grafana   │
                                          │ Dashboards  │
                                          └─────────────┘
```

## Configuration Integration

### Required Configuration Sections

The prometheus-exporter requires these sections in your `configuration.ini`:

```ini
[project]
project_dir = /homino
logging_dir = /var/log/automate-home
redis_host = 172.31.10.219
redis_port = 6379
my_node_name = brain
other_nodes_names = ws, graphite-feeder, prometheus-exporter

[prometheus_exporter]
logging_level = INFO
pushgateway_host = http://pushgateway
pushgateway_port = 9091
job_name = automate_home
node_name = prometheus-exporter
other_nodes_names = brain
```

### Configuration Options

| Section | Option | Description | Example |
|---------|--------|-------------|---------|
| `[project]` | `other_nodes_names` | Must include `prometheus-exporter` | `ws, prometheus-exporter` |
| `[prometheus_exporter]` | `node_name` | Unique identifier for this exporter | `prometheus-exporter` |
| `[prometheus_exporter]` | `other_nodes_names` | Other nodes to listen to (usually `brain`) | `brain` |
| `[prometheus_exporter]` | `pushgateway_host` | Pushgateway URL | `http://pushgateway` |
| `[prometheus_exporter]` | `pushgateway_port` | Pushgateway port | `9091` |
| `[prometheus_exporter]` | `job_name` | Prometheus job name | `automate_home` |
| `[prometheus_exporter]` | `logging_level` | Log verbosity | `DEBUG`, `INFO`, `WARNING`, `ERROR` |

## Docker Integration

### Dockerfile

The prometheus-exporter is included in the main automate-home Docker image:

**Dockerfile.dev:**
```dockerfile
RUN git clone https://github.com/majamassarini/automate-prometheus-exporter.git --branch main
RUN cd automate-prometheus-exporter && pip install .
```

**Dockerfile.local:**
```dockerfile
COPY automate-prometheus-exporter automate-prometheus-exporter
RUN sh -c "cd automate-prometheus-exporter && python setup.py install"
```

### Docker Compose

The prometheus-exporter runs as a separate container:

```yaml
prometheus-exporter:
  image: automate-home:dev
  container_name: home-prometheus-exporter
  depends_on:
    - redis
    - pushgateway
  volumes:
    - ./automate-home/my-home/configuration.docker.ini:/homino/configuration.ini:ro
  command: >
    python -m prometheus_exporter
    --configuration-file /homino/configuration.ini
  networks:
    qnet-static-eth0:
      ipv4_address: 172.31.10.215
```

## Event Flow

### 1. Appliance State Change

When an appliance state changes (e.g., temperature sensor reading):

```python
# In automate-home brain
thermometer = Thermometer("bedroom_thermometer")
old_state = thermometer.state
new_state = old_state.next(home.event.temperature.Event(22.5))

# State is persisted to Redis
redis.publish("appliance:update", thermometer.serialize())
```

### 2. Redis Pub/Sub

The prometheus-exporter subscribes to Redis channels:

```python
# In prometheus-exporter
async def on_appliance_updated(self, new_appliance):
    appliance = self._home_resources.appliances.find(new_appliance.name)
    old_state, new_state = appliance.update(new_appliance)
    # Process state change...
```

### 3. Event Processing

Events are extracted from state changes:

```python
for event in new_state - old_state:
    # event = temperature.Event(22.5)
    event_handler = prometheus_exporter.handler.event.registry.mapper[event.__class__]
    appliance_handler = prometheus_exporter.handler.appliance.registry.mapper[appliance.__class__]

    metric_name = f"{appliance_handler.metric_prefix}_{event_handler.metric_suffix}"
    # metric_name = "home_sensor_temperature_float_value"

    value = event_handler.get_value()
    # value = 22.5
```

### 4. Metric Push

Metrics are pushed to Pushgateway:

```python
gauge = Gauge(
    "home_sensor_temperature_float_value",
    "Temperature in degrees Celsius",
    labelnames=["appliance"],
    registry=self._registry
)
gauge.labels(appliance="bedroom_thermometer").set(22.5)

push_to_gateway(
    "pushgateway:9091",
    job="automate_home",
    registry=self._registry
)
```

### 5. Prometheus Scrape

Prometheus scrapes Pushgateway:

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'automate_home'
    honor_labels: true
    static_configs:
      - targets: ['pushgateway:9091']
```

### 6. Grafana Visualization

Grafana queries Prometheus:

```promql
home_sensor_temperature_float_value{appliance="bedroom_thermometer"}
```

## Handler Architecture

### Appliance Handlers

Located in `prometheus_exporter/handler/appliance/`:

```python
class Handler(metaclass=Registry):
    KLASS = home.appliance.sensor.thermometer.Appliance
    METRIC_PREFIX = "home_sensor_temperature"
    DESCRIPTION = "Temperature in degrees Celsius"

    def get_value(self):
        # Extract value from appliance state
        return None  # Or specific value
```

### Event Handlers

Located in `prometheus_exporter/handler/event/`:

```python
class Handler(metaclass=Registry):
    KLASS = float
    METRIC_SUFFIX = "float_value"
    DESCRIPTION = "Float value from event"

    def get_value(self):
        return float(self._event)
```

### Adding New Handlers

**For a new appliance type:**

```python
# prometheus_exporter/handler/appliance/sensor/humidity.py
import home
from prometheus_exporter.handler.appliance.handler import Handler as Parent

class Handler(Parent):
    KLASS = home.appliance.sensor.humidity.Appliance
    METRIC_PREFIX = "home_sensor_humidity"
    DESCRIPTION = "Relative humidity percentage"

    def get_value(self):
        # If you want appliance-level metric
        return self._appliance.state.humidity
```

**For a new event type:**

```python
# prometheus_exporter/handler/event/bool_handler.py
from prometheus_exporter.handler.event.handler import Handler as Parent

class Handler(Parent):
    KLASS = bool
    METRIC_SUFFIX = "bool_value"
    DESCRIPTION = "Boolean value (0 or 1)"

    def get_value(self):
        return 1 if self._event else 0
```

## Metrics Format

All metrics follow this naming convention:

```
{prefix}_{suffix}{appliance="{name}"}
```

Examples:

```
home_sensor_temperature_float_value{appliance="bedroom_thermometer"} 22.5
home_sensor_power_float_value{appliance="kitchen_powermeter"} 150.0
home_sensor_lux_float_value{appliance="living_room_luxmeter"} 450.0
```

## Dependencies

The prometheus-exporter depends on:

- **automate-home**: Core framework with state machines
- **prometheus-client**: Python client for Prometheus
- **Redis**: Message bus for inter-process communication

## Deployment Checklist

- [ ] Update `Dockerfile.dev` or `Dockerfile.local`
- [ ] Add `[prometheus_exporter]` section to configuration.ini
- [ ] Add `prometheus-exporter` to `other_nodes_names` in `[project]` section
- [ ] Update docker-compose.yml with prometheus-exporter container
- [ ] Deploy Pushgateway container
- [ ] Deploy Prometheus container
- [ ] Deploy Grafana container
- [ ] Verify containers are running
- [ ] Check prometheus-exporter logs for successful pushes
- [ ] Verify metrics in Prometheus
- [ ] View dashboards in Grafana

## Troubleshooting

### No metrics in Prometheus

1. Check prometheus-exporter logs:
   ```bash
   docker logs home-prometheus-exporter
   ```
   Look for: "Pushed metrics to Pushgateway"

2. Check Pushgateway directly:
   ```bash
   curl http://localhost:9091/metrics | grep home_
   ```

3. Verify Redis connection:
   ```bash
   docker logs home-prometheus-exporter | grep -i redis
   ```

### Metrics not updating

1. Verify brain is publishing to Redis:
   ```bash
   docker logs home-brain | grep -i appliance
   ```

2. Check prometheus-exporter is subscribed:
   ```bash
   docker logs home-prometheus-exporter | grep -i "Updated metric"
   ```

3. Verify handlers are loaded:
   ```python
   # In prometheus-exporter container
   python -c "import prometheus_exporter.handler.appliance.registry as r; print(r.registry)"
   ```

## Performance Considerations

- Metrics are pushed on every state change (real-time)
- Pushgateway holds metrics until Prometheus scrapes (default 15s)
- No historical data is lost during container restarts (Prometheus retains data)
- Registry is kept in memory (lightweight)

## Security

- No authentication on Pushgateway by default
- Configure network policies to restrict access
- Use Grafana authentication for dashboard access
- Consider Prometheus authentication if exposing externally
