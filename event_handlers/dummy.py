class EventHandler:

    def __init__(self):
        self.modules = None
        self.stop    = None
        self.start   = None


    def on_press(self, key):
        try:
            if key.char == "q":
                self.stop()
                
        except AttributeError: pass
            
        print(key)


    @property
    def on_release(self):
        # this only gets called once when initializing the listener
        return None 
