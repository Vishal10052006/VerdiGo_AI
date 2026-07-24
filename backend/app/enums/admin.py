from enum import Enum


class AdminRoleEnum(str, Enum):
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"