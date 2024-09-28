import argparse
import logging
import sys

log = logging.getLogger(__name__)


def read_argument(dev_options=None):
    """
    This function is for reading the arguments passed in the command line

    :return: ``argument string``

    """
    try:
        parser = argparse.ArgumentParser(description='Supporting Rally, Rally Camera, MeetUp and Rally Bar')
        parser.add_argument('--dev', choices=dev_options)
        args = parser.parse_args()
        log.debug(args)
        return args.dev

    except Exception as e:
        log.error(e)


def get_name_of_os():
    """
    This method gets the name of operating system

    :return: ``name of the operating system``
    :rtype: ``string``
    """
    try:
        os = sys.platform
        if os.startswith('darwin'):
            platform = 'macos'
        elif os.startswith('darwin'):
            platform = 'linux'
        else:
            platform = 'windows'

        return platform

    except Exception as e:
        logging.error(e)




