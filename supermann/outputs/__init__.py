"""
This package describes output classes for collected metrics.

supermann.outputs.base
-----------------------------

Base class for all outputs. New outputs should inherit it

.. automodule:: supermann.outputs.base
    :members:
    :show-inheritance:


supermann.outputs.debug
---------------------------------

Debug output, just log metrics in stderr

.. automodule:: supermann.outputs.debug
    :members:
    :undoc-members:
    :show-inheritance:

supermann.outputs.influx
-----------------------------------

Write metrics into influxdb

.. automodule:: supermann.outputs.influx
    :members:
    :undoc-members:
    :show-inheritance:

supermann.outputs.riemann
--------------------------------

Write metrics into riemann. Used as default

.. automodule:: supermann.outputs.riemann
    :members:
    :undoc-members:
    :show-inheritance:

"""
import imp
import importlib
import logging

from supermann.outputs.riemann import RiemannOutput


def load_output(classPath):

    #by default return Riemann output
    if not classPath:
        return RiemannOutput()

    mdl, cls = classPath.rsplit(".", 1)

    try:
        return getattr(importlib.import_module(mdl), cls)()
    except:
        logging.exception("Can't load module %s", classPath)
        raise AttributeError("Module {} not found".format(classPath))

