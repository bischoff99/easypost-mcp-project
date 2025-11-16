from __future__ import annotations


def sanitize_error(error: Exception) -> str:
    """Remove sensitive data from error messages."""
    import re

    msg = str(error)

    # Remove API keys (EasyPost format: EZAKxxxx or EZTKxxxx)
    msg = re.sub(
        r"(EZAK|EZTK)[a-zA-Z0-9]{32,}", "[API_KEY_REDACTED]", msg, flags=re.IGNORECASE
    )

    # Remove Bearer tokens
    msg = re.sub(r"Bearer\s+[^\s]+", "Bearer [REDACTED]", msg)

    # Remove email addresses from error messages
    msg = re.sub(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "[EMAIL_REDACTED]", msg
    )

    # Truncate if too long
    if len(msg) > 200:
        msg = msg[:200] + "..."

    return msg
