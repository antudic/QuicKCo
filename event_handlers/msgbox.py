from tkinter.simpledialog import askstring as msgBoxPrompt
from tkinter.messagebox import showinfo

class EventHandler:

    def __init__(self):
        self.modules = None
        self.driver  = None


    def __call__(self, key):
        if key["is_press"] and key["vkName"] == "PAUSE":
            response = msgBoxPrompt("QuicKCo", "Enter Command")

            if not response:
                return
            # ^ if the string is empty (the user hit the cancel button)
            
            cmdName = response.split(" ")[0]
            cmdArgs = response.replace(cmdName+" ", "", 1)

            try:
                if (text := self.driver.modules[cmdName](cmdArgs)):
                    showinfo(
                        self.driver.modules[cmdName].name,
                        text
                        )
                
            except KeyError: pass


    def start(self):
        self.driver.start()
