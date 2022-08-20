import tkinter as tk
from pynput.keyboard import Key

def setClipboard(string, saveClipboard=True):
    root = tk.Tk()
    root.withdraw()
    
    if saveClipboard:
        try: print(root.clipboard_get())
        except tk._tkinter.TclError: pass
    
    root.clipboard_clear()
    root.clipboard_append(string)

class EventHandler:

    def __init__(self):
        self.modules = None
        self.stop    = None
        self.start   = None

        self.listen = False
        self.chars  = ""
        self.actionKeys = {
            Key.pause: self.on_pause,
            Key.enter: self.on_enter}


    def on_press(self, key):
        if self.listen:
            if key == Key.space:
                self.chars+= " "
                return
            
            elif key == Key.backspace:
                self.chars = self.chars[:-1]
                return
                        
            try: self.chars+= key.char
            except (AttributeError,
                    TypeError): pass

        try: self.actionKeys[key]()
        except KeyError: pass

            
    @property
    def on_release(self):
        return None
        # tells driver to ignore key releases


    def on_pause(self):
        self.listen = True


    def on_enter(self):
        if self.listen:
            cmdName = self.chars.split(" ")[0]
            cmdArgs = self.chars.replace(cmdName+" ", "", 1)
            self.listen = False
            self.chars  = ""

            try:
                if (text := self.modules[cmdName](cmdArgs)):
                    setClipboard(text, True)
                
            except KeyError: return
