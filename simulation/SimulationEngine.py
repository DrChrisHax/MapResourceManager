from algorithms.analyzeIncident import checkForIncident
from algorithms.dijkstra import dijkstraPath
from simulation.Scheduler import Scheduler
from ui.gui import SimulationUI
from models.Incident import Incident, IncidentType, Department

class SimulationEngine:
    def __init__(self):
        self.inGameTime = 0 #In game minutes
        self.maxTime = 24 * 60 #24 hours per simulated day
        self.day = 1
        

        self.resources = {
            Department.POLICE: [1, 2, 3, 4],
            Department.FIRE: [5, 6, 7, 8],
            Department.MEDICAL: [9, 10, 11, 12]
        }

        self.stationNodes = {
            Department.POLICE: 1,
            Department.FIRE: 1,
            Department.MEDICAL: 1
        }

        self.scheduler = Scheduler(engine=self, stationNodes=self.stationNodes)
        self.ui = SimulationUI(self)

        #A dictionary to convert the simulation engine graph
        #back into the graph form the UI wants
        self.intToNodeId = {
            int(node.nodeId.split()[1]): node.nodeId
            for node in self.ui.nodes
        }

        self.graphDict = self.ConvertGraphToIntGraph(self.ui.graphToDict())

    def run(self):
        self.ui.run()

    def Start(self):
        #Starts the simulation for the in game day
        self.RunGameLoop()

    def RunGameLoop(self):
        while self.inGameTime < self.maxTime:
            #1. Fetch new incidents
            incidents = checkForIncident(self.inGameTime)
            for inc in incidents:
                self.scheduler.AddIncident(inc)
                print(f"[Engine] time={self.inGameTime} received incident: {inc}")
            
            #2. Schedule and dispatch resources
            dispatches = self.scheduler.Schedule(currentTime=self.inGameTime)
            if dispatches:
                for dispatch in dispatches:
                    inc, v, path, cost = dispatch
                    
                    #3. Update GUI dashboard
                    policeCount, fireCount, medicalCount = self.getAvailableResourceCounts()
                    self.ui.updateDashboard(
                        policeCount,
                        fireCount,
                        medicalCount,
                        address=f"{inc.locationName} @ node {inc.location}",
                        incidentType=inc.incidentType.name,
                        time=self.formatTime(),
                        priority=str(inc.resourceNeed)
                    )

                    #4. Send the resource out
                    print(f"[Engine] time={self.inGameTime} Dispatch Vehicle {v.id} -> Path: {path}, Cost: {cost}")
                    guiGraphPath = [self.intToNodeId[n] for n in path] #Convert engine graph nodes to gui graph nodes
                    self.ui.animatePath(guiGraphPath, v.department)


            self.inGameTime += 1

        print(f"[Engine] Day {self.day} done")
        self.day += 1

    def ConvertGraphToIntGraph(self, graph: dict[str, list[tuple[str, int]]]) -> dict[int, list[tuple[int, int]]]:
        intGraph: dict[int, list[tuple[int, int]]] = {}

        for uLabel, num in graph.items():
            u = int(uLabel.split()[1])
            for vLabel, w in num:
                v = int(vLabel.split()[1])
                intGraph.setdefault(u, []).append((v, w))
                intGraph.setdefault(v, []).append((u, w))
        return intGraph

    def TravelPathAndCost(self, startNode: int, endNode: int):
        path, cost = dijkstraPath(self.graphDict, startNode, endNode)
        return path, cost
    
    def formatTime(self) -> str:
        hrs, mins = divmod(self.inGameTime, 60)
        return f"{hrs:02d}:{mins:02d}"

    def getAvailableResourceCounts(self) -> tuple[int,int,int]:
        """Returns (#police_free, #fire_free, #medical_free)"""
        free = [v for v in self.scheduler.vehicles if v.availableAt <= self.inGameTime]
        police = sum(1 for v in free if v.department == Department.POLICE)
        fire   = sum(1 for v in free if v.department == Department.FIRE)
        med    = sum(1 for v in free if v.department == Department.MEDICAL)
        return police, fire, med
        
    