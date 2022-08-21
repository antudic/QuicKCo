# QuicKCo

QuicKCo (short for Quick Keyboard Commands) is a simple Python framework to allow users to run code based on keyboard inputs. 
QuicKCo leverages a very modular design (the driver program only taking up 44 lines of code excluding empty lines). 

The general paradigm of QuicKCo is for the code to be broken up into 3 separate parts; the **Driver** code that captures the
keyboard inputs and sends them to the selected **Event Handler** which parses the text using any method it wants to 
finally make **Module** calls along with any arguments the user has sent to the Module. The Module can then do things
such as opening websites or getting the current temperature outside.

The included Module and Event Handlers are there to serve as guideposts as to how to structure Event Handlers and Modules.
If you are planning on creating your own Module or Event Handler, I suggest reading the ``dummy.py`` Event Handler as well
as the ``eval.py`` Module to get a feel for how the connections between the various programs work.

The planned future of the project is to eventually have some way to browse user-submitted Event Handlers and Modules 
but until then, I will happily accept any pull requests into this repository as long as the code is functional (and 
is at least somewhat well-written)

The ``driver.py`` file is *not* finished and will be getting changes in the future.
