class PermissionException(Exception):
    pass

class UserNotFoundException(Exception):
    pass

class UserCannotBePromotedException(Exception):
    pass

class UserCannotBeDemotedException(Exception):
    pass

class InvalidPaginationParams(Exception):
    pass