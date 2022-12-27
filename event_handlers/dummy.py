class EventHandler: 

    # This is the defalt class that will be 
    # imported through the driver.py program

    def __init__(self):
        self.modules = None
        # This gets set to a dictionary with the key being the module name
        # and the value being the callable function

        self.driver  = None
        # This gets set to the driver instance itself, allowing access to the
        #  `start` and `stop` methods, to start or stop listening to keystrokes


    def __call__(self, key):
        # This function gets called whenever a key is pressed and whenever a
        # key is released.
        # 
        # The `key` parameter is a dictionary containing the data from the
        # KBDLLHOOKSTRUCT plus an additional "char" parameter: 
        # "char": The character that has been pressed (can be None) (str)
        # "scan": The windows scan code (is often 0) (int)
        # "vkCode": The windows vkCode (int)
        # "vkName": The windows vkName (str or None)
        # "is_press": True if press, False if release (bool)
        # 
        # More info: https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-kbdllhookstruct

        if key["is_press"]: print(key)
        
        if key["char"] == "q":
            print("Stopping :)")
            self.driver.stop()
            # Stops listening to keyboard events. In this EventHandler, there 
            # is no way to start the listener again.


    def start(self):
        # This is the first function called after all modules have been loaded 
        # and the listener is ready to go

        self.driver.start(suppress=False)
        # Start listening to keyboard presses without suppressing them
        # Setting suppress to True will block the rest of the system from 
        # receiving them
