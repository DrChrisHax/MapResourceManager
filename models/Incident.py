from enum import Enum, auto
from typing import Tuple

class IncidentType(Enum):
    NONE = auto()
    HOUSE_FIRE = auto()
    SMOKE = auto()
    GAS_LEAK = auto()
    EXPLOSION = auto()
    DROWNING = auto()
    OVERDOSE = auto()
    HEART_ATTACK = auto()
    BREATHING_ISSUE = auto()
    UNCONSCIOUS = auto()
    INJURY = auto()
    COLLISION = auto()
    ACCIDENT = auto()
    ROBBERY = auto()
    THEFT = auto()
    BREAK_IN = auto()
    ASSAULT = auto()
    BOMB_THREAT = auto()

class Department(Enum):
    NONE = auto()
    FIRE = auto()
    MEDICAL = auto()
    POLICE = auto()

class Incident:
    def __init__(
        self,
        incidentType: IncidentType,
        department: Department,     
        location: int,              #Node Number
        locationName: str,          #Building Name (for story purposes)
        time: int,                  #Time event happened at
        resourceNeed: int,          #Vehichle Cost
        timeNeed: int,               #Time Cost
        description: str,
    ):
        self.incidentType   = incidentType
        self.department     = department
        self.location       = location
        self.locationName   = locationName
        self.time           = time         
        self.resourceNeed   = resourceNeed
        self.timeNeed = timeNeed
        self.description = description

    def __repr__(self) -> str:
        if isinstance(self.department, set):
            dept_names = ", ".join(d.name for d in self.department)
        else:
            dept_names = self.department.name
        return (
            f"<Incident "
            f"type={self.incidentType.name} "
            f"dept={dept_names} "
            f"Vehicle need={self.resourceNeed} "
            f"Time need={self.timeNeed} "
            f"location={self.locationName} at node {self.location}>"
        )