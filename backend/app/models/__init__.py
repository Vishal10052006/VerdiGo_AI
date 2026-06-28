"""
Application Models

Imports all SQLAlchemy models.

These imports ensure Alembic discovers all models during
migration autogeneration.
"""

from .user import User
from .otp import OTP
from .farmer_profile import FarmerProfile
from .farm import Farm