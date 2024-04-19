# QuicKCo (Windows application)

QuicKCo (short for Quick Keyboard Commands) is a simple Python framework to allow users to run code based on keyboard inputs. 
QuicKCo leverages a very modular design (the ``driver.py`` file (the only part of the project intended to be non-modular) only 
taking up 37 SLOC). 

The general paradigm of QuicKCo is for the code to be broken up into 3 separate parts; the **Driver** code that captures the
keyboard inputs and sends them to the selected **Event Handler** (available event handlers in this repo are `dummy`, `msgbox` and `hidden`) 
which parses the text using any method it wants to finally make **Module** calls along with any arguments the user has sent to the Module. 
The Module can then do things such as executing python code or fetching current temperature data from an API. The Event Handler also 
provides a default method of returning Module reponses to the user.

The included Modules and Event Handlers are there to serve as guideposts as to how they're supposed to be structured.
If you are planning on creating your own Module or Event Handler, I suggest reading the ``dummy.py`` Event Handler as well
as the ``eval.py`` Module to get a feel for how the connections between the various programs are intended to work.

This framework is designed to be as unrestrictive to the developer as possible and there is nothing stopping you from chaining
multiple Modules or Event Handlers together or even throwing the Driver -> Event Handler -> Module hierarchy out the window.

The planned future of the project is to eventually have some way to browse user-submitted/created Event Handlers and Modules 
but until then, I will happily accept any pull requests into this repository as long as the code is functional (and 
is at least somewhat well-written according to my (very low) standards).
