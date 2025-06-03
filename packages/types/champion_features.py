from enum import Enum

##### Gameplay identity
class DamageProfile(Enum):
    BURST = 0
    SUSTAINED = 1
    POKE = 2
    DOT = 3
    # Maybe some others
    
class Range(Enum):
    MELEE = 0
    SHORT_RANGE = 1
    LONG_RANGE = 2
    
class Mobility(Enum):
    DASH_BASED = 0
    BLINK = 1
    SPEED_BOOST = 2
    IMMOBILE = 3
    
class CCProfile(Enum):
    HARD_CC = 0
    SOFT_CC = 1
    NO_CC = 2
    
class PrimaryScaling(Enum):
    AP = 0
    AD = 1
    MIXED = 2
    
class ScalingAxis(Enum): 
    # Each enumerate values are closely correlated. 
    # Ex : the more levels you have, the higher rank your ult is. 
    # So if your scaling is "based" on your ult, it's somewhat also based on levels aswell
    ITEM_DEPENDENT = 0
    LEVEL_DEPENDENT = 1
    ULT_BASED = 2

class TeamRole(Enum):
    ENGAGE = 0
    PEEL = 1
    ZONE_CONTROL = 2
    BACKLINE_DIVE = 3
    OBJECTIVE_CONTROL = 4
    
class SynergyProfile(Enum):
    AOE_COMP = 0
    POKE_COMP = 1
    DIVE_COMP = 2
    SPLIT_COMP = 3
    # Maybe some others
    
class PowerCurve(Enum):
    EARLY_GAME = 0
    MID_GAME = 1
    LATE_GAME = 2


##### Strategic Role in Teamplay
class EngagePotential(Enum):
    NONE = 0
    MODERATE = 1
    HIGH = 2
    
class PeelCapability(Enum):
    NONE = 0
    MODERATE = 1
    HIGH = 2

class WaveClear(Enum):
    FAST = 0
    SLOW = 1
    CONDITIONAL = 2 # For champions that requires items to have proper waveclear (ex : fiora before/after tiamat)
    
class ObjectiveControl(Enum):
    ZONING = 0
    SMITE_CONTROL = 1
    AOE_DENIAL = 2
    NONE = 3
    
class ZoneControl(Enum):
    STRONG = 0
    MODERATE = 1
    NONE = 3
    
class RoamingPower(Enum):
    GLOBAL = 0
    LOCAL = 1
    NONE = 2
    
class DuelPower(Enum):
    STRONG = 0
    MODERATE = 1
    NONE = 2