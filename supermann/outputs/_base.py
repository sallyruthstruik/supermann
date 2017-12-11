from ConfigParser import ConfigParser


class BaseOutput(object):
    section_name = None

    def __init__(self):
        assert self.section_name, "Section name is required!"

    def init(self, **params):
        """
        This method called in Supermann initialization and should initialize output.
        """
        raise NotImplemented

    def __enter__(self):
        """
        By default do nothing
        :return:
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        By default do nothing
        """

    def init_from_configparser(self, parser):
        #type: (ConfigParser)->None
        assert self.section_name, "Section name is required!"

        self.init(**dict(parser.items(self.section_name)))

    def event(self, **data):
        """
        Should save one event metric data in bulk
        :param data:
        """
        raise NotImplementedError

    def flush(self):
        """
        Should send bulk in output
        """
        raise NotImplementedError