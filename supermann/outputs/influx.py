import logging
import re
import socket

import sys

import supermann
from supermann.outputs.base import BaseOutput

from influxdb.client import InfluxDBClient

class Point(object):
    point = None
    tags = None
    measurement = None

    def __init__(self, **k):
        self.__dict__.update(k)

    def __repr__(self):
        return "Point({}, {}, {})".format(self.measurement, self.point, self.tags)

    def to_influx(self):
        return dict(
            measurement=self.measurement,
            tags=self.tags,
            fields=self.point
        )


class InfluxOutput(BaseOutput):
    """
    Writes point into influxdb.

    Each system metrics will be written into separated measurement.
    All process metrics will be tagged by process_name and will be written into
    separated metrics.

    All points will be tagged with hostname.
    """
    section_name = "influx"

    hostname = socket.gethostname()
    processname_pattern = re.compile(r"^process:([^\:]+):(.*)")

    def init(self, **params):
        self.influx_client = InfluxDBClient(
            **params
        )

        supermann.utils.getLogger(self).info(
            "Using InfluxOutput with params %s", str(params))

    def __init__(self):
        super(InfluxOutput, self).__init__()
        self.bulk = []

    def flush(self):
        self.influx_client.write_points(
            [p.to_influx() for p in self.bulk]
        )

        self.bulk = []

    def event(self, **data):

        try:
            service = data["service"]
            metric = data["metric_f"]
        except:
            return

        if service.startswith("system"):
            self.bulk.append(Point(
                measurement=service,
                point={
                    "metric": metric
                },
                tags={
                    "hostname": self.hostname
                }
            ))
        elif service.startswith("process"):
            processname, tail = self.processname_pattern.findall(service)[0]

            self.bulk.append(Point(
                measurement="process:{}".format(tail),
                point={
                    "metric": metric
                },
                tags={
                    "hostname": self.hostname,
                    "process": processname
                }
            ))
