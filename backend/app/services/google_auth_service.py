"""
Google OAuth Service

Verifies Google-issued ID tokens server-side (signature + issuer +
audience checks via Google's public key set — never trust a client-
supplied token without this) and extracts the verified identity
claims needed for find-or-create user logic.

Module:
Phase 1 → Module 1 → Authentication (Google OAuth)

Author: VerdiGO Backend Team
"""

from google.auth.transport import requests as google_requests
from google.oauth2 import id_token as google_id_token

from app.config.settings import settings
from app.core.exceptions import UnauthorizedException


def verify_google_id_token(token: str) -> dict:
    """
    Verify a Google ID token and return its claims.

    Raises:
        UnauthorizedException if the token is invalid, expired, or
        was not issued for this app's OAuth client ID (audience check
        — without this, a token issued for a DIFFERENT app could be
        replayed here).
    """

    if not settings.GOOGLE_OAUTH_CLIENT_ID:
        raise UnauthorizedException(
            message="Google login is not configured on this server."
        )

    try:
        claims = google_id_token.verify_oauth2_token(
            token,
            google_requests.Request(),
            settings.GOOGLE_OAUTH_CLIENT_ID,
        )
    except ValueError as exc:
        raise UnauthorizedException(message="Invalid Google credential.") from exc

    if claims.get("iss") not in ("accounts.google.com", "https://accounts.google.com"):
        raise UnauthorizedException(message="Invalid token issuer.")

    if not claims.get("email_verified", False):
        raise UnauthorizedException(
            message="Google account email is not verified."
        )

    return claims
