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

from .weather_cache import WeatherCache
from .weather_advisory import WeatherAdvisory
from .weather_provider_request_log import WeatherProviderRequestLog

from .refresh_token import RefreshToken
from .token_blacklist import TokenBlacklist

from .crop import Crop
from .crop_recommendation import CropRecommendation, CropRecommendationItem

from .crop import Crop
from .crop_recommendation import CropRecommendation, CropRecommendationItem

from .chat import ChatConversation, ChatMessage
from .chat_rate_limit import ChatRateLimit

from .disease_detection import DiseaseDetection

from .feature_rate_limit import FeatureRateLimit
from .notification import Notification

from .admin_user import AdminUser