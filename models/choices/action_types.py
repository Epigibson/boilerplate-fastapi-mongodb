from enum import Enum


class ActionTypes(str, Enum):
    """
    Actions that can be performed on the system.
    """
    create = "create"
    delete = "delete"
    update = "update"
    read = "read"
    login = "login"
    logout = "logout"
