from sqlmodel import Field, Relationship, SQLModel


# Shared properties
# TODO replace email str with EmailStr when sqlmodel supports it
class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str


# TODO replace email str with EmailStr when sqlmodel supports it
class UserRegister(SQLModel):
    email: str
    password: str
    full_name: str | None = None


# Properties to receive via API on update, all are optional
# TODO replace email str with EmailStr when sqlmodel supports it
class UserUpdate(UserBase):
    email: str | None = None  # type: ignore
    password: str | None = None


# TODO replace email str with EmailStr when sqlmodel supports it
class UserUpdateMe(SQLModel):
    full_name: str | None = None
    email: str | None = None


class UpdatePassword(SQLModel):
    current_password: str
    new_password: str


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    items: list["Item"] = Relationship(back_populates="owner")
    polls: list["Poll"] = Relationship(back_populates="owner")


# Properties to return via API, id is always required
class UserOut(UserBase):
    id: int


class UsersOut(SQLModel):
    data: list[UserOut]
    count: int


# Shared properties
class ItemBase(SQLModel):
    title: str
    description: str | None = None


# Properties to receive on item creation
class ItemCreate(ItemBase):
    title: str


# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: str | None = None  # type: ignore


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    owner_id: int | None = Field(default=None, foreign_key="user.id", nullable=False)
    owner: User | None = Relationship(back_populates="items")


# Properties to return via API, id is always required
class ItemOut(ItemBase):
    id: int
    owner_id: int


class ItemsOut(SQLModel):
    data: list[ItemOut]
    count: int


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: int | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str


class DotaHeroe(SQLModel):
    id: int
    name: str
    localized_name: str
    primary_attr: str
    attack_type: str
    roles: list[str]


class DotaHeroes(SQLModel):
    data: list[DotaHeroe]
    count: int


class PollBase(SQLModel):
    hero_id: int
    hero_name: str
    team: str
    team_id: int
    player_name: str | None = None
    description: str | None = None


class PollCreate(PollBase):
    pass


class PollUpdate(PollBase):
    pass


# Database model, database table inferred from class name
class Poll(PollBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hero_id: int
    hero_name: str
    team: str
    team_id: int
    player_name: str | None = None
    description: str | None = None
    owner_id: int | None = Field(default=None, foreign_key="user.id", nullable=False)
    owner: User | None = Relationship(back_populates="polls")


# Properties to return via API, id is always required
class PollOut(PollBase):
    id: int
    owner_id: int


class PollsOut(SQLModel):
    data: list[PollOut]
    count: int


class Teams(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    id_team: int
    name_team: str


class TeamsOut(SQLModel):
    data: list[Teams]
    count: int
