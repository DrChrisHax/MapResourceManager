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
            f"loc={self.currentLocation} free_at={self.availableAt}>"
        )
    
class Scheduler:
    def __init__(self, engine: 'SimulationEngine', stationNodes: Dict[Department, int]):
        self.engine = engine
        self.stationNodes = stationNodes
        self.pending: List[Incident] = []      #A list of unhandled incidents
        self.vehicles: List[Vehicle] = []      #All vehicles at our disposal

        #Init Vehicle objects from eninge.resources
        #engine resource keys are dept names in lowercase
        for dept, vehList in engine.resources.items():
            station = stationNodes.get(dept, 0)
            for idx in range(len(vehList)):
                vid = len(self.vehicles)
                v = Vehicle(vehicleID=vid, department=dept, stationNode=station)
                self.vehicles.append(v)

    def AddIncident(self, incident: Incident) -> None:
        self.pending.append(incident)
    
    def FindAvailableVehicles(self, currentTime: int) -> List[Vehicle]:
        return [v for v in self.vehicles if v.availableAt <= currentTime]
    
    def ComputerTravelTime(self, vehicle: Vehicle, node: int) -> int:
        temp = self.engine.TravelCostAndPath(vehicle.currentLocation, node)
        
        if temp is None:
            # Handle the case where temp is None
            print(f"Error: TravelCostAndPath returned None for vehicle at {vehicle.currentLocation} to node {node}")
            return 0  # Or handle with a fallback value like 0 or some appropriate response
        
        return temp[0]  # Proceed as usual if temp is not None


    def RateIncident(self, incident: Incident, avail: List[Vehicle], currentTime: int):
        #Scores incidents for schedling
        #Metrics include:
        #Vehicle resources needs
        #Time for furthest chosen last needed vehicle to get there
        #Time the incident will take to be completed
        #TIme the incident has been active for

        k = incident.resourceNeed

        #Only check vehicles for the correct department
        deptAvail = [v for v in avail if v.department == incident.department]
        if k > len(avail):
            return None #Not enough resources to help this incident
        
        #Grab the integer node for the location object
        nodeID = incident.location

        travelList = []
        for v in deptAvail:
            t = self.ComputerTravelTime(v, nodeID)
            if t is not None:
                travelList.append((v, t))
        if len(travelList) < k:
            return None
        
        #Score
        print(f"travelList before sorting: {travelList}")
        travelList.sort(key=lambda pair: int(pair[1]) if isinstance(pair[1], str) else pair[1])
        chosen = travelList[:k]
        chosenVehicles, times = zip(*chosen)
        maxTravel = times[-1]
        waitTime = currentTime - incident.time
        totalTime = maxTravel + incident.timeNeed
        score = k * (waitTime + 1) / totalTime

        return incident, list(chosenVehicles), score, maxTravel, waitTime
    
    def SelectIncidents(self, currentTime: int) -> List[Tuple[Incident, List[Vehicle]]]:
        avail = self.FindAvailableVehicles(currentTime)
        scored = []
        for inc in self.pending:
            r = self.RateIncident(inc, avail, currentTime)
            if r:
                scored.append(r)

        #Sort by best score, then fewer vehicles (tie-breaker)
        scored.sort(key=lambda x: (x[2], -len(x[1])), reverse=True)

        assignments = []
        used = set()
        cap = len(avail)

        for inc, vehs, _, _, _ in scored:
            if any(v in used for v in vehs):
                continue
            if len(used) + len(vehs) > cap:
                continue
            assignments.append((inc, vehs))
            for v in vehs:
                used.add(v)

        return assignments
    
    def Schedule(self, currentTime: int) -> List[Tuple[int, int]]:
        #Assigns vehicles to as many incidents as possible this tick
        #returns a list of (startNode, endNode) for each dispatched vehicle

        dispatches: List[Tuple[int, int]] =[]
        assignments = self.SelectIncidents(currentTime)

        for inc, vehs in assignments:
            travelTime = [self.ComputerTravelTime(v, inc.location) for v in vehs]
            maxTravel = max(travelTime) if travelTime else 0

            #Each vehicle needs to travel there, wait for everyone to be there, then service the incident
            serviceEnd = currentTime + maxTravel + inc.timeNeed

            for v in vehs:
                start = v.currentLocation
                #Mark vehicle unavailable until serviceEnd
                v.availableAt = serviceEnd
                v.currentLocation = inc.location
                dispatches.append((start, inc.location))

            self.pending.remove(inc)

        return dispatches

