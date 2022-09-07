class EventHandler:


    def __init__(self):
        self.modules = None
        self.driver  = None


    def __call__(self, key):
        if key["is_press"]: print(key)
        
        if key["char"] == "q":
            print("Stopping :)")
            self.driver.stop()


    def start(self):
        self.driver.start(suppress=False)
