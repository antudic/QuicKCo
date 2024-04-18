import time

class Module:

    def __init__(self):
        self.name    = "d8str"
        self.modules = None
        # ^ this is to access other modules

    def __call__(self, args):
        return time.strftime("%Y-%m-%d %H%M")