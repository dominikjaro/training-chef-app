from typing import Optional
from sqlmodel import Field, SQLModel, Relationship

# ---------------------------------------------------------
# TABLE 1: USER (Identity)
# ---------------------------------------------------------
# This will hold the identity info from Google later
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    # google_sub is the unique ID Google gives a user
    google_sub: str = Field(unique=True, index=True) 
    full_name: Optional[str] = None
    
    # Relationship: A User can have one Profile.
    # 'profile' will be usable as a Python object (e.g., my_user.profile)
    profile: Optional["Profile"] = Relationship(back_populates="user")


# ---------------------------------------------------------
# TABLE 2: PROFILE (Cycling Data)
# ---------------------------------------------------------
# This now belongs to a specific User
class Profile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    currentWeight: float
    height: float
    ftp: int
    bodyType: str

    # Foreign Key: Links this physical profile row to a User ID in the other table
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    
    # Relationship link back to the User object
    user: Optional[User] = Relationship(back_populates="profile")