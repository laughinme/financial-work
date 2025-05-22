class InvalidLibraryError(ValueError):
    def __init__(self, error_text):
        super().__init__(error_text)
