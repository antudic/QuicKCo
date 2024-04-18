import _listener as listener

import sys
import json

from importlib import import_module


class QuicKCo:

    def __init__(self, loadConfig=True):
        self.config       = None
        self.eventHandler = None
        self.modules      = None
        self.keyThread    = None

        if loadConfig: self.loadConfig()

        self.start = listener.start
        self.stop  = listener.stop


    def loadConfig(self, verbose=False):
        if verbose: print("Reading config file...")
        with open("./config.json", "r") as file:
            self.config = json.load(file)

        if verbose: print("Loading modules...")
        self.modules = {}

        for moduleName in self.config["modules"]:
            module = import_module(moduleName).Module()
            self.modules[module.name] = module
            module.modules = self.modules
            if verbose: print(f"Loaded {moduleName}")

        if verbose: print("Loading event handler...")
        eventHandler = import_module(self.config["eventHandler"])
        listener.eventHandler = eventHandler.EventHandler()
        
        listener.eventHandler.driver = self
        
        if verbose: print("Done.")


if __name__ == "__main__":
    sys.path.append("./event_handlers")
    sys.path.append("./modules")
    qkc = QuicKCo()

    print("Running in mode: " + qkc.config["eventHandler"])
    
    listener.eventHandler.start()
