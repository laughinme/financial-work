from dataclasses import dataclass


@dataclass
class AddUserModel:
    password: str
    secret: str

    email: str = None
    phone_number: str = None


@dataclass
class UserModel:
    id: str

    email: str
    phone_number: str

    password: str
    secure_code: str
    secret: str
