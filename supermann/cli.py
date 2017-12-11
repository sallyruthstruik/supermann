"""Command line entry points to supermann using click"""

from __future__ import absolute_import

import logging
from ConfigParser import ConfigParser, SafeConfigParser, NoOptionError

import click
import sys

import supermann.core
import supermann.utils


@click.command()
@click.version_option(version=supermann.__version__)
@click.option(
    '-l', '--log-level', default='INFO',
    type=click.Choice(supermann.utils.LOG_LEVELS.keys()),
    help="One of CRITICAL, ERROR, WARNING, INFO, DEBUG.")
@click.option(
    '--system/--no-system', default=True,
    help='Enable or disable system metrics.')
@click.argument(
    'host', type=click.STRING, default='localhost', envvar='RIEMANN_HOST')
@click.argument(
    'port', type=click.INT, default=5555, envvar='RIEMANN_PORT')
def main(log_level, host, port, system):
    """The main entry point for Supermann"""
    # Log messages are sent to stderr, and Supervisor takes care of the rest

    try:
        supermann.utils.configure_logging(log_level)

        s = supermann.core.Supermann(host, port)
        if system:
            s.connect_system_metrics()
        s.connect_process_metrics()
        s.run()
    except Exception as e:
        logging.exception("Exception running supermann: %s", e)
        raise e, None, sys.exc_traceback



@click.command()
@click.argument('config', type=click.File('r'))
def from_file(config):
    """An alternate entry point that reads arguments from a file."""
    main.main(args=config.read().split())

@click.command()
@click.argument('config', type=click.File('r'))
def from_config(config):
    """
    Entry point that reads arguments from a .ini config
    """

    parser = ConfigParser()
    parser.readfp(config)

    try:
        log_level = parser.get("supermann", "log_level")
    except NoOptionError:
        log_level = "INFO"

    try:
        system = parser.getboolean("supermann", "system")
    except NoOptionError:
        system = True

    try:
        output_class = parser.get("supermann", "output_class")
    except NoOptionError:
        output_class = "supermann.outputs.riemann.RiemannOutput"

    try:
        supermann.utils.configure_logging(log_level)

        s = supermann.core.Supermann()
        s.load_output(output_class, parser)

        if system:
            s.connect_system_metrics()
        s.connect_process_metrics()
        s.run()
    except Exception as e:
        logging.exception("Exception running supermann: %s", e)
        raise e, None, sys.exc_traceback
