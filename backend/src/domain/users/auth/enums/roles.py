from enum import IntEnum


class Role(IntEnum):
    """User scopes depends on role"""
    
    GUEST = 10
    ADMIN = 100
