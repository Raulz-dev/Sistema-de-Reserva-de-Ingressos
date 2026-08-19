class InvalidUserNameError(Exception):
    pass


class InvalidUserEmailError(Exception):
    pass


class InvalidUserPasswordHashError(Exception):
    pass


class InvalidUserRoleError(Exception):
    pass


class UserEmailAlreadyExistsError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


class PasswordMismatchError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass
