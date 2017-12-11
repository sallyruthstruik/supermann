from __future__ import absolute_import

import os.path

import click.testing
import mock

import supermann.cli
from supermann.core import Supermann
from supermann.outputs import load_output
from supermann.outputs.debug import DebugOutput
from supermann.outputs.riemann import RiemannOutput


def main(args=[], env=None, command=supermann.cli.main):

    runner = click.testing.CliRunner()
    result = runner.invoke(command, args, env=env)
    print result.output
    assert result.exit_code == 0
    return result


@mock.patch('supermann.core.Supermann', autospec=True)
class TestCLI(object):
    def test_main_with_all(self, supermann_cls):
        main(['--log-level', 'INFO', 'localhost', '5555'])
        supermann_cls.assert_called_with('localhost', 5555)

    def test_main_with_args(self, supermann_cls):
        main(['example.com', '6666'])
        supermann_cls.assert_called_with(u'example.com', 6666)

    def test_custom_output_class(self, supermann_cls):
        assert load_output('supermann.outputs.riemann.RiemannOutput').__class__ is RiemannOutput
        assert load_output('supermann.outputs.debug.DebugOutput').__class__ is DebugOutput

    def test_main_with_some_args(self, supermann_cls):
        main(['example.com'])
        supermann_cls.assert_called_with('example.com', 5555)

    def test_main_without_args(self, supermann_cls):
        main()
        supermann_cls.assert_called_with('localhost', 5555)

    def test_system_flag(self, supermann_cls):
        main(['--system'])
        assert supermann_cls.return_value.connect_system_metrics.called

    def test_no_system_flag(self, supermann_cls):
        main(['--no-system'])
        assert not supermann_cls.return_value.connect_system_metrics.called

    def test_main_with_env(self, supermann_cls):
        main(env={
            'RIEMANN_HOST': 'example.com',
            'RIEMANN_PORT': '6666'
        })
        supermann_cls.assert_called_with('example.com', 6666)

    @mock.patch('supermann.utils.configure_logging')
    def test_log_level(self, configure_logging, supermann_cls):
        main(['--log-level', 'WARNING'])
        configure_logging.assert_called_with('WARNING')

    @mock.patch('supermann.utils.configure_logging')
    def test_from_file(self, configure_logging, supermann_cls):
        path = os.path.join(os.path.dirname(__file__), 'supermann.args')
        main([path], command=supermann.cli.from_file)
        configure_logging.assert_called_with('DEBUG')
        supermann_cls.assert_called_with('example.com', 6666)

@mock.patch("supermann.supervisor.Supervisor")
@mock.patch("supermann.outputs.influx.InfluxOutput.init")
def test_from_config(output_cls, supervisor_cls):

    path = os.path.join(os.path.dirname(__file__), 'supermann.ini')

    main([path], command=supermann.cli.from_config)

    output_cls.assert_called_with(database='database', host='test.host', password='password', username='admin')

