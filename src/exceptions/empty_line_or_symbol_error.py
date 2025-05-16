class EmptyLineOrSymbolError(Exception):
    def __init__(self, message="No symbol or line segments are defined"):
        self.message = message
        super().__init__(self.message)