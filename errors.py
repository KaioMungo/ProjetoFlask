class EmptyStringError(Exception):
    pass

class IdNotExist(Exception):
    def __init__(self, message):
        self.message = message