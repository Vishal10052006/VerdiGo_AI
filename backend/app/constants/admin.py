"""
Admin Panel Constants

Module: Phase 1 → Module 10 → Admin Panel
Author: VerdiGO Backend Team
"""

# ============================================================================
# Admin Login Rate Limiting
#
# Stricter than OTP send limiting — this guards the highest-privilege
# account type in the system (bcrypt password auth, not OTP), and was
# previously completely unthrottled: an attacker could brute-force an
# admin password with unlimited attempts against /admin/auth/login.
# ============================================================================

ADMIN_LOGIN_MAX_ATTEMPTS_PER_WINDOW = 5
ADMIN_LOGIN_WINDOW_SECONDS = 900  # 15 minutes