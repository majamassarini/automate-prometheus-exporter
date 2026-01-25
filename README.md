# automate-prometheus-exporter

Prometheus metrics exporter for the [automate-home project](https://github.com/majamassarini/automate-home).

## Overview

This project exports home automation metrics from the automate-home system to Prometheus via Pushgateway. It listens to Redis for appliance state changes and pushes metrics in real-time.

## Architecture

```
┌──────────────┐      ┌─────────────┐      ┌──────────────┐      ┌───────────┐
│ automate-home│─────▶│    Redis    │─────▶│ prometheus-  │─────▶│Pushgateway│
│    (brain)   │      │             │      │   exporter   │      │           │
└──────────────┘      └─────────────┘      └──────────────┘      └─────┬─────┘
                                                                         │
                                                                         ▼
                                                                   ┌──────────┐
                                                                   │Prometheus│
                                                                   └────┬─────┘
                                                                        │
                                                                        ▼
                                                                   ┌─────────┐
                                                                   │ Grafana │
                                                                   └─────────┘
```

## Features

- **Real-time metrics**: Pushes metrics immediately when appliance states change
- **Extensible handlers**: Easy to add new appliance and event types
- **Push model**: Uses Prometheus Pushgateway for batch job metrics
- **Multi-protocol support**: Works with all automate-home protocols (KNX, Sonos, Home Assistant, etc.)

## Metrics Exported

### Sensor Metrics
- `home_sensor_temperature_float_value{appliance="..."}` - Temperature in °C
- `home_sensor_power_float_value{appliance="..."}` - Power consumption/production in Watts
- `home_sensor_lux_float_value{appliance="..."}` - Light intensity in lux

### Appliance Metrics
- Light brightness, hue, saturation
- Sound player volume
- Curtain positions
- And more...

All metrics include the `appliance` label with the appliance name for easy filtering and grouping in Grafana.

## Installation

```bash
pip install -e .
```

## Configuration

Add the following options to your automate-home configuration file:

```ini
[prometheus_exporter]
node_name = prometheus-exporter-1
other_nodes_names =
pushgateway_host = http://pushgateway
pushgateway_port = 9091
job_name = automate_home
logging_level = INFO
```

## Usage

### Standalone

```bash
python -m prometheus_exporter --configuration-file /path/to/configuration.ini
```

### Docker

See the main homino docker-compose.yml for container setup.

## Development

### Adding New Appliance Handlers

Create a new handler in `prometheus_exporter/handler/appliance/`:

```python
import home
from prometheus_exporter.handler.appliance.handler import Handler as Parent

class Handler(Parent):
    KLASS = home.appliance.your.Appliance
    METRIC_PREFIX = "home_your_metric"
    DESCRIPTION = "Your metric description"

    def get_value(self):
        # Extract value from self._appliance.state
        return some_value
```

### Adding New Event Handlers

Create a new handler in `prometheus_exporter/handler/event/`:

```python
from prometheus_exporter.handler.event.handler import Handler as Parent

class Handler(Parent):
    KLASS = YourEventClass
    METRIC_SUFFIX = "your_metric"
    DESCRIPTION = "Your event description"

    def get_value(self):
        return self._event.value
```

## Grafana Integration

Prometheus metrics can be visualized in Grafana:

1. Add Prometheus as a data source
2. Import dashboards or create custom ones
3. Use PromQL queries like:
   ```promql
   home_sensor_temperature_float_value{appliance="bedroom_thermometer"}
   ```

## License

GNU General Public License v3.0

## Author

Maja Massarini <maja.massarini@gmail.com>

## Links

- [automate-home](https://github.com/majamassarini/automate-home)
- [Prometheus](https://prometheus.io/)
- [Prometheus Pushgateway](https://github.com/prometheus/pushgateway)
- [Grafana](https://grafana.com/)
