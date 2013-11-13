"""A Supervisor event listener for Riemann"""

from __future__ import absolute_import, unicode_literals, print_function

import sys

import supermann.riemann.client
import supermann.supervisor.events
import supermann.supervisor.listener

__version__ = '0.1.0'
__author__ = 'Sam Clements <sam.clements@datasift.com>'
__all__ = ['Supermann']


class Supermann(object):
    """The Supermann event listener"""

    def __init__(self, reserve_stdin=True, reserve_stdout=True):
        self.supervisor = supermann.supervisor.listener.EventListener()

        # As stdin/stdout are used to communicate with Supervisor,
        # reserve them by replacing the sys attributes with None
        if reserve_stdin:
            sys.stdin = None
        if reserve_stdout:
            sys.stdout = None

    def run(self):
        """Wait for events from Supervisor and pass them to recive()"""
        while True:
            event = self.supervisor.wait()
            self.recive(event)
            self.supervisor.ok()

    def recive(self, event):
        """Handle each event from supervisor"""
        if isinstance(event, supermann.supervisor.events.TICK):
            print("Tick at {0} (every {1} seconds)".format(
                event.when, event.frequency), file=sys.stderr)
        else:
            print("Recived {event!r}".format(event=event), file=sys.stderr)


def test(value=0):
    with supermann.riemann.client.UDPClient('localhost', 5555) as client:
        client.send_event(
            service='supermann',
            description="Supermann test",
            tags=['supermann', 'test'],
            state='ok',
            metric_f=value)


def main():
    supermann = Supermann()
    supermann.run()