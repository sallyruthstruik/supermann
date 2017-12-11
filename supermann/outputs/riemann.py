import riemann_client
from riemann_client.client import QueuedClient

import supermann
from supermann.outputs.base import BaseOutput

class RiemannOutput(BaseOutput):
    section_name = "riemann"

    def init(self, **params):
        """
        Initialization of output

        :param host: required, host
        :param port: required, port

        Other params are depend on kind of output
        """
        self.host = params["host"]
        self.port = params["port"]
        self.riemann = riemann_client.client.QueuedClient(
            riemann_client.transport.TCPTransport(self.host, self.port))  #type: QueuedClient

        supermann.utils.getLogger(self).info(
            "Using Riemann protobuf server at {0}:{1}".format(self.host, self.port))

    def __enter__(self):
        self.riemann.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.riemann.__exit__(exc_type, exc_val, exc_tb)

    def event(self, **data):
        self.riemann.event(**data)

    def flush(self):
        self.riemann.flush()