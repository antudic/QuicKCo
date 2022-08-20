import os
import sys
import time
import json
import ctypes

from importlib import import_module
from pynput.keyboard import Key, Listener


def CustomShortcut(shortcut):
    try:
        x = open('Shortcuts.txt')
        location = 'Shortcuts.txt'
    except FileNotFoundError:
        try:
            x = open('./Other/Shortcuts.txt')
            location = './Other/Shortcuts.txt'
        except FileNotFoundError:
            location = False
    if location is not False:
        x = open(location, 'r')
        y = x.read()
        x.close()

    else:
        ctypes.windll.user32.MessageBoxW(0, "Shortcuts.txt not found. Please re-install the program.", "HFCKS", 0x10)


class QuicKCo:

    def __init__(self, loadConfig=True):
        self.config       = None
        self.eventHandler = None
        self.modules      = None
        self.keyThread    = None

        if loadConfig: self.loadConfig()


    def loadConfig(self, verbose=False):
        if verbose: print("Reading config file...")
        with open("config.json", "r") as file:
            self.config = json.load(file)

        if verbose: print("Loading modules...")
        self.modules = {}

        for moduleName in self.config["modules"]:
            module = import_module(moduleName).Module()
            self.modules[module.name] = module

        if verbose: print("Loading event handler...")
        eventHandler = import_module(self.config["eventHandler"])
        self.eventHandler = eventHandler.EventHandler()
        
        self.eventHandler.modules = self.modules
        self.eventHandler.start   = self.start
        self.eventHandler.stop    = self.stop
        
        if verbose: print("Done.")


    def start(self):
        with Listener(
                on_press=self.eventHandler.on_press,
                on_release=self.eventHandler.on_release
                ) as self.keyThread:
            
            self.keyThread.join()


    def stop(self):
        self.keyThread.stop()
        
        


if __name__ == "__main__":
    sys.path.append("./event_handlers")
    sys.path.append("./modules")
    qkc = QuicKCo()
    qkc.start()
