class CinemaNotFoundError(Exception):
    pass


class RoomNotFoundError(Exception):
    pass


class CinemaNameAlreadyExistsError(Exception):
    pass


class RoomNameAlreadyExistsError(Exception):
    pass


class InvalidCinemaError(Exception):
    pass


class InvalidRoomError(Exception):
    pass
