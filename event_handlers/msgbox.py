import pymsgbox

class EventHandler:


    def __init__(self):
        self.modules = None
        self.driver  = None


    def __call__(self, key):
        if key["is_press"] and key["vkName"] == "PAUSE":
            print("asd")
            response = pymsgbox.prompt("Enter Command")

            if not response:
                print("exiting early")
                return
            
            cmdName = response.split(" ")[0]
            cmdArgs = response.replace(cmdName+" ", "", 1)

            try:
                if (text := self.driver.modules[cmdName](cmdArgs)):
                    pymsgbox.alert(
                        text,
                        self.driver.modules[cmdName].name
                        )
                
            except KeyError: pass


    def start(self):
        self.driver.start(suppress=False)
