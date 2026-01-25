"""
Test that all imports work correctly in prometheus_exporter package.

Note: These tests require automate-home to be installed, as the import structure
follows the same pattern as graphite-feeder which eagerly loads all submodules.
"""
import unittest
import sys

try:
    import home
    HOME_AVAILABLE = True
except ImportError:
    HOME_AVAILABLE = False


@unittest.skipUnless(HOME_AVAILABLE, "automate-home not installed")
class TestImports(unittest.TestCase):
    """Test module imports."""

    def test_import_main_package(self):
        """Test importing the main package."""
        import prometheus_exporter
        self.assertIsNotNone(prometheus_exporter)
        self.assertTrue(hasattr(prometheus_exporter, '__version__'))
        self.assertTrue(hasattr(prometheus_exporter, 'conf'))
        self.assertTrue(hasattr(prometheus_exporter, 'handler'))

    def test_import_conf_submodule(self):
        """Test importing conf submodule."""
        import prometheus_exporter
        self.assertIsNotNone(prometheus_exporter.conf)
        self.assertTrue(hasattr(prometheus_exporter.conf, 'default_logging_configuration'))

    def test_import_handler_submodules(self):
        """Test accessing handler submodules."""
        import prometheus_exporter
        self.assertTrue(hasattr(prometheus_exporter.handler, 'appliance'))
        self.assertTrue(hasattr(prometheus_exporter.handler, 'event'))

    def test_import_handler_appliance_registry(self):
        """Test importing handler.appliance.registry."""
        import prometheus_exporter
        # registry is actually a dict (Registry.mapper)
        self.assertIsNotNone(prometheus_exporter.handler.appliance.registry)
        self.assertIsInstance(prometheus_exporter.handler.appliance.registry, dict)

    def test_import_handler_event_registry(self):
        """Test importing handler.event.registry."""
        import prometheus_exporter
        # registry is actually a dict (Registry.mapper)
        self.assertIsNotNone(prometheus_exporter.handler.event.registry)
        self.assertIsInstance(prometheus_exporter.handler.event.registry, dict)

    def test_conf_function_accessible(self):
        """Test that conf.default_logging_configuration is callable."""
        import prometheus_exporter
        self.assertTrue(callable(prometheus_exporter.conf.default_logging_configuration))

        # Test calling it
        config = prometheus_exporter.conf.default_logging_configuration('/tmp')
        self.assertIsInstance(config, dict)
        self.assertIn('version', config)
        self.assertIn('handlers', config)

    def test_handler_types_imported(self):
        """Test that handler types are imported."""
        import prometheus_exporter

        # Check appliance handlers
        self.assertIsNotNone(prometheus_exporter.handler.appliance.sensor)

        # Check event handlers
        self.assertTrue(hasattr(prometheus_exporter.handler.event, 'Handler'))
        self.assertTrue(hasattr(prometheus_exporter.handler.event, 'FloatHandler'))
        self.assertTrue(hasattr(prometheus_exporter.handler.event, 'IntHandler'))


if __name__ == '__main__':
    unittest.main()
