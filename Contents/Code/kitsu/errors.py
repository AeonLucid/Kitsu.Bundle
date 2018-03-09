class KitsuError(Exception):
    """
    Just making it more clear where the error comes from
    """
    pass


class ServerError(KitsuError):
    """
    Raised when we encounter an error retrieving information from the server.
    """
    def __init__(self, message=None, code=500):
        self.msg = message
        self.code = code

    def __repr__(self):
        if self.msg:
            return "Server Error encounted.\nCode: {}\nMessage: {}".format(self.code, self.msg)
        else:
            return "Encountered a server error attempting to access information."
