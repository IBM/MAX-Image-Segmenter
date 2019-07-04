import json
import os


def debug(msg, adict=None):
    """
        Print a debug message if environment variable
        MAX_DEBUG is set
        :param msg: message to print
        :type msg: str

        :param adict: if specified, adict will be printed
        :type adict: dict
    """
    if os.environ.get('MAX_DEBUG', None) is not None:
        print('[DEBUG] {}'.format(msg))
        if adict:
            print(json.dumps(adict, indent=2))
