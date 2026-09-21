class InvalidSessionError(ValueError):
    pass


class SessionNotFoundError(Exception):
    pass


class SessionConflictError(Exception):
    pass


class SessionMovieNotFoundError(Exception):
    pass


class SessionRoomNotFoundError(Exception):
    pass
