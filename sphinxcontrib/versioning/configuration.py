"""Store run-time configuration in a globally accessible class."""


class GlobalConfig(object):
    """The global config for the project. Should be updated only at the beginning of run-time.

    Only define values set by external configuration sources.
    """

    NO_BANNER = False
