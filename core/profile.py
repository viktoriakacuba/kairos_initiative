from pydantic import BaseModel
from core.modes import Mode

class UserProfile(BaseModel):
    id: int
    email: str
    mode: Mode = Mode.DEFAULT
    is_subscribed: bool = False
    memory_enabled: bool = False
    archetype_id: str = "kairos"

def get_user_by_id(user_id: str) -> UserProfile:
    return UserProfile(
        id=int(user_id), 
        email="anonymous@kairos.ai",
        mode=Mode.DEFAULT,
        is_subscribed=False,
        memory_enabled=False,
        archetype_id="kairos"
    )
