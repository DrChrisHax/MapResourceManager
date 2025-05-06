from algorithms.analyzeIncident import checkForIncident
from algorithms.dijkstra import dijkstraPath
from simulation.Scheduler import Scheduler
from ui.gui import SimulationUI
from models.Incident import Incident, IncidentType, Department

class SimulationEngine:
    def __init__(self):
        self.inGameTime = 0 #In game minutes
        self.maxTime = 5 #24 * 60 #24 hours per simulated day
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
        dummy_incident = Incident(
                    incidentType=IncidentType.HOUSE_FIRE,
                    department=Department.FIRE,
                    location=10,
                    locationName="Test Station",
                    time=2,
                    resourceNeed=1,
                    timeNeed=15
                )

        while self.inGameTime < self.maxTime:
            #Generate a log and see if it results
            #in new incident(s) to deal with
            #If it does, add it to the queue of incidents

            try:
                raw_services, raw_address = response(self.inGameTime)
            except:
                pass

            
            if self.inGameTime == 2:
                self.scheduler.AddIncident(dummy_incident)

            dispatches = self.scheduler.Schedule(currentTime=self.inGameTime)
            if dispatches:
                print(f"[Engine] t={self.inGameTime} dispatches: {dispatches}")


            self.inGameTime += 1

        print(f"Day {self.day} done")
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


    def TravelCostAndPath(self, startNode: int, endNode: int) -> int:
        path, cost = dijkstraPath(self.graphDict, startNode, endNode)
        return path
    
        
    