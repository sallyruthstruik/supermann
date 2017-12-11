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

