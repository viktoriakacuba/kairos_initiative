from fastapi import HTTPException
from core.profile import UserProfile
from core.modes import Mode

def require_subscription(user: UserProfile, allowed_modes: list[Mode]):
    if user.mode not in allowed_modes:
        raise HTTPException(status_code=403, detail="Upgrade required for this feature.")
