"""
Test that all imports work correctly in prometheus_exporter package.
"""

import unittest


class TestImports(unittest.TestCase):
    """Test module imports."""

    def test_import_main_package(self):
        """Test importing the main package."""
        import prometheus_exporter

        self.assertIsNotNone(prometheus_exporter)
        self.assertTrue(hasattr(prometheus_exporter, "__version__"))
        self.assertTrue(hasattr(prometheus_exporter, "conf"))

    def test_import_conf_submodule(self):
        """Test importing conf submodule."""
        import prometheus_exporter

        self.assertIsNotNone(prometheus_exporter.conf)
        self.assertTrue(
            hasattr(prometheus_exporter.conf, "default_logging_configuration")
        )

    def test_conf_function_accessible(self):
        """Test that conf.default_logging_configuration is callable."""
        import prometheus_exporter

        self.assertTrue(
            callable(prometheus_exporter.conf.default_logging_configuration)
        )

        config = prometheus_exporter.conf.default_logging_configuration("/tmp")
        self.assertIsInstance(config, dict)
        self.assertIn("version", config)
        self.assertIn("handlers", config)


if __name__ == "__main__":
    unittest.main()
