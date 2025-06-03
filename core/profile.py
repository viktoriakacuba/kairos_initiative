from pydantic import BaseModel
from core.modes import Mode

class UserProfile(BaseModel):
    id: int
    email: str
    mode: Mode = Mode.DEFAULT
    is_subscribed: bool = False
    memory_enabled: bool = False
    archetype_id: str = "kairos"

# Мок — позже заменим на real auth
def get_mock_user() -> UserProfile:
    return UserProfile(
        id=1,
        email="mock@kairos.ai",
        mode=Mode.DEFAULT,
        is_subscribed=False,
        memory_enabled=False
    )
