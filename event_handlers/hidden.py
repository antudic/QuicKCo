import tkinter as tk

def getCb(): # get clipboard
    root = tk.Tk()
    root.withdraw()

    try: return root.clipboard_get()
    except tk._tkinter.TclError: return ""

def setCb(string, saveClipboard=True): # set clipboard
    root = tk.Tk()
    root.withdraw()
    
    if saveClipboard:
        try: print(root.clipboard_get())
        except tk._tkinter.TclError: pass
    
    root.clipboard_clear()
    root.clipboard_append(string)

class EventHandler:

    def __init__(self):
        self.driver    = None

        self.listen = False
        self.chars  = ""
        self.actionKeys = {
            "PAUSE": self.on_pause,
            "RETURN": self.on_enter}


    def start(self):
        self.driver.start()

    
    def __call__(self, key):
        if not key["is_press"]: return

        try: self.actionKeys[key["vkName"]]()
        except KeyError: pass
        
        if self.listen:
            if key["vkName"] == "BACK":
                self.chars = self.chars[:-1]
                return

            if key["char"]: self.chars+= key["char"]


    def on_pause(self):
        self.listen = True
        self.driver.stop()
        self.driver.start(suppress=True)


    def on_enter(self):
        if self.listen:
            self.driver.stop()

            self.chars = self.chars.replace("\x16", getCb())
            
            cmdName = self.chars.split(" ")[0]
            cmdArgs = self.chars.replace(cmdName+" ", "", 1)
            
            self.listen = False
            self.chars  = ""

            try:
                if (text := self.driver.modules[cmdName](cmdArgs)):
                    setCb(text, True)
                
            except KeyError: pass
            self.driver.start()
