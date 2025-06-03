from enum import Enum

class Mode(str, Enum):
    DEFAULT = "default"          # Freemium
    FOUNDER = "founder"          # Premium
    STRATEGIST = "strategist"    # Premium
    INVESTOR = "investor"        # Premium
