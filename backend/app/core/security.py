from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer

# ============================================================
# JWT Bearer Authentication
#
# Unlike OAuth2PasswordBearer, HTTPBearer simply accepts:
#
# Authorization: Bearer <JWT>
#
# This is perfect for OTP-based authentication because
# users already receive a JWT after /auth/verify-otp.
# ============================================================

bearer_scheme = HTTPBearer(
    auto_error=True
)