from setuptools import setup, find_packages

setup(
    name="automate-prometheus-exporter",
    version="0.1.0",
    description="Prometheus metrics exporter for automate-home project",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Maja Massarini",
    author_email="maja.massarini@gmail.com",
    url="https://github.com/majamassarini/automate-prometheus-exporter",
    packages=find_packages(),
    install_requires=[
        "prometheus-client>=0.19.0",
    ],
    # Note: automate-home is not on PyPI, install it separately:
    # git clone https://github.com/majamassarini/automate-home.git
    # cd automate-home && pip install .
    python_requires=">=3.10",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Home Automation",
    ],
    entry_points={
        "console_scripts": [
            "prometheus-exporter=prometheus_exporter.__main__:main",
        ],
    },
)
