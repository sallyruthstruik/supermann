import logging

from supermann.outputs.base import BaseOutput
import supermann

class DebugOutput(BaseOutput):
    section_name = "debug_output"

    def init(self, **params):
        supermann.utils.getLogger(self).info(
            "Using DebugOutput")

    def flush(self):
        pass

    def event(self, **data):
        logging.error(str(data))

