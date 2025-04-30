from typing import List, Tuple, Dict
from models.Incident import Incident, Department

class Vehicle:
    def __init__(self, vehicleID: int, department: Department, stationNode: int):
        self.id = vehicleID
        self.department = department
        self.stationNode = stationNode
        self.currentLocation = stationNode      #Vehicles start at the station and move from there
        self.availableAt = 0                    #Game time when the vehicle is free

    def __repr__(self):
        return (
            f"<Vehicle id={self.id} dept={self.department.name} "
            f"loc={self.current_location} free_at={self.available_at}>"
        )
    
class Scheduler:
    def __init__(self, engine: 'SimulationEngine', stationNodes: Dict[Department, int]):
        self.engine = engine
        self.stationNodes = stationNodes
        self.pending: List[Incident] = []      #A list of unhandled incidents
        self.vehicles: List[Vehicle] = []      #All vehicles at our disposal

        #Init Vehicle objects from eninge.resources
        #engine resource keys are dept names in lowercase
        for deptKey, vehList in engine.resources.items():
            dept = Department[deptKey.upper()]
            station = stationNodes.get(dept, 0)
            for idx in range(len(vehList)):
                vid = len(self.vehicles)
                v = Vehicle(vehicleID=vid, department=dept, stationNode=station)
                self.vehicles.append(v)

    def AddIncident(self, incident: Incident) -> None:
        self.pending.append(incident)

    def Schedule(self, currentTime: int) -> List[Tuple[int, int]]:
        """
        Assign available vehicles to pending incidents at the given game time.
        Returns a list of (startNode, endNode) tuples for dispatch

        - A vehicle is available if its availableAt <= currentTime
        - Travel time to incident  engine.travelCost(start, end)
        - Handing time per incident = incident.timeNeed
        - Vehicle.currentLocation updates to incident.location after passing through
          all relevant nodes
        """ 