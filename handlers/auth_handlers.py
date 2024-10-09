from abc import ABC, abstractmethod

class auth_handlers(ABC):

    def __init__(self, next_handler = None):
        self.next_hander = next_handler

    @abstractmethod
    def handler(self, request):
        pass

    def set_next(self, next_handler):
        self.next_hander = next_handler

        return self.next_hander
