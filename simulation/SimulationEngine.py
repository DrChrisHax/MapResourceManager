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
        self.graphDict = self.ConvertGraphToIntGraph(self.ui.graphToDict())

    def run(self):
        self.ui.run()

    def Start(self):
        #Starts the simulation for the in game day
        self.RunGameLoop()

    def RunGameLoop(self):
        while self.inGameTime < self.maxTime:
            incidents = checkForIncident(self.inGameTime)

            for inc in incidents:
                self.scheduler.AddIncident(inc)
                print(f"[Engine] time={self.inGameTime} received incident: {inc}")
            
            dispatches = self.scheduler.Schedule(currentTime=self.inGameTime)
            if dispatches:
                for dispatch in dispatches:
                    vehicleID, path, cost = dispatch
                    print(f"[Engine] time={self.inGameTime} Dispatch Vehicle {vehicleID} -> Path: {path}, Cost: {cost}")


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
    
        
    