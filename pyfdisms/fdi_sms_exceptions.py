class BadRequest(Exception):
    error_message = "Bad Request: malformed request or missing required parameters."

    def __init__(self, error_message=error_message):
        super().__init__(error_message)


class Unauthorized(Exception):
    error_message = "Unauthorized: Well, well, well... it seems your token went out for a quick coffee break and never came back - try generating a new one."

    def __init__(self, error_message=error_message):
        super().__init__(error_message)


class Forbidden(Exception):
    error_message = "Forbidden: You are trying to access a resource for which you don't have proper access rights."

    def __init__(self, error_message=error_message):
        super().__init__(error_message)


class NotFound(Exception):
    error_message = "Not Found: You are trying to access a resource that does not exist"

    def __init__(self, error_message=error_message):
        super().__init__(error_message)


class UnprocessableEntity(Exception):
    error_message = "Unprocessable Entity: You provided all the required parameters but they are not proper for the request."

    def __init__(self, error_message=error_message):
        super().__init__(error_message)


class InternalServerError(Exception):
    error_message = "Internal Server Error: We had a glitch in our servers. Retry the request in a little while or contact support."

    def __init__(self, error_message=error_message):
        super().__init__(error_message)


class ServiceUnavailable(Exception):
    error_message = "Service Unavailable: We’re temporarily offline for maintenance. Please try again later."

    def __init__(self, error_message=error_message):
        super().__init__(error_message)


class UnknownError(Exception):

    def __init__(self, error):
        super().__init__("Whoooops! Don't know what happend: " + error)

