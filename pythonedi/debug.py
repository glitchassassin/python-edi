"""
Debug printer

Handles logging at different debug levels
"""

from colorama import Fore, init
init()

class DebugMaster(object):
    """ Auto-instantiated as Debug to provide a single point of contact """
    def __init__(self):
        self.level = 3
        self.tags = {
            "ERROR":   "{}[ ERROR ]{} ".format(Fore.RED, Fore.RESET),
            "WARNING": "{}[WARNING]{} ".format(Fore.YELLOW, Fore.RESET),
            "MESSAGE": "{}[MESSAGE]{} ".format(Fore.CYAN, Fore.RESET)
        }

    def log(self, message, level=1):
        """ Creates a custom message at the specified level """
        if level <= self.level:
            print("\n" + message)

    def log_error(self, message):
        """ Creates an error-level log messsage """
        self.log(self.tags["ERROR"] + message, 1)

    def log_warning(self, message):
        """ Creates a warning-level log messsage """
        self.log(self.tags["WARNING"] + message, 2)

    def log_message(self, message):
        """ Creates a message-level log messsage """
        self.log(self.tags["MESSAGE"] + message, 3)

Debug = DebugMaster()
