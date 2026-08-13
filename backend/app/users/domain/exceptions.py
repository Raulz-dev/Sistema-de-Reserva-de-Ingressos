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


class UserDontExist(Exception):
    pass
