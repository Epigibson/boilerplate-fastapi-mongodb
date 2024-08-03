from enum import Enum


class Usertype(str, Enum):
    admin = "Admin"
    user = "User"
    athlete = "Athlete"
    couch = "Couch"
    manager = "Manager"
