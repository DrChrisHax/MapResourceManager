from enum import Enum, auto
from typing import Tuple

class IncidentType(Enum):
    NONE            = auto() #Used for non-incidents
    HOUSE_FIRE      = auto()
    HEART_ATTACK    = auto()
    ROBBERY         = auto()
    #Add more later

class Department(Enum):
    NONE        = auto() #Used for non-incidents
    FIRE        = auto()
    MEDICAL     = auto()
    POLICE      = auto()

class Incident:
    def __init__(
        self,
        incidentType: IncidentType,
        department: Department,     
        location: int,              #Node Number
        locationName: str,          #Building Name (for story purposes)
        time: int,                  #Time event happened at
        resourceNeed: int,          #Vehichle Cost
        timeNeed: int               #Time Cost
    ):
        self.incidentType   = incidentType
        self.department     = department
        self.location       = location
        self.locationName   = locationName
        self.time           = time         
        self.resourceNeed   = resourceNeed
        self.timeNeed = timeNeed

    def __repr__(self) -> str:
        return (
            f"<Incident "
            f"type={self.incidentType.name} "
            f"dept={self.department.name} "
            f"severity={self.severity.name} "
            f"time={self.time} "
            f"location={self.locationName} at {self.location}>"
        )