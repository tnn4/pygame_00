from __future__ import annotations
from abc import ABC, abstractmethod


# the command interface
"""
ABC= Abstract Base Class
I= interface
"""
class ICommand(ABC):
    @abstractmethod
    def execute():
        pass
    #fed

# Any class may serve as a receiver
class Receiver():
    """
    Any class may serve as a receiver
    """
    pass
    def do_something():
        print("I do something")
    #fed
#class

class DerivedReceiver(Receiver):
    def __init__(self):
        print("I'm a derived class")
    #fed
    
#class



# Command tells receiver to execute something
# command's init takes a receiver
class Command(ICommand):
    
    def __init__(self, receiver: Receiver):
        self._receiver = receiver
    #fed

    def execute(self):
        self._receiver.do_something()
    #fed
#class

class Invoker():
    # invoker
    _on_start  = None
    _on_end    = None

    def set_on_start(self, command: Command):
        self._on_start=command
    #fed

    def set_on_end(self, command: Command):
        self._on_end=command
    #fed

    def do_something(self):
        
        if isinstance(self._on_start, Command):
            # do something on start
            self._on_start.execute()
        #fi

        # do other logic

        if isinstance(self._on_end, Command):
            # do something on end
            self._on_end.execute()
    #fed    
#class