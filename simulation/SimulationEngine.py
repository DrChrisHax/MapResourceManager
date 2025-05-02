from algorithms.analyzeIncident import response
from algorithms.dijkstra import dijkstraPath
from simulation.Scheduler import Scheduler
from ui.gui import SimulationUI

class SimulationEngine:
    def __init__(self):
        self.inGameTime = 0 #In game minutes
        self.maxTime = 24 * 60 #24 hours per simulated day
        self.day = 1
        

        self.resources = {
            'police': [1, 2, 3, 4],
            'fire': [5, 6, 7, 8],
            'medical': [9, 10, 11, 12]
        }

        self.stationNodes = {
            'police': 1,
            'fire': 1,
            'medical': 1
        }

        self.scheduler = Scheduler(engine=self, stationNodes=self.stationNodes)
        self.ui = SimulationUI(self)
        self.graphDict = self.ui.graphToDict()

    def run(self):
        self.ui.run()

    def Start(self):
        #Starts the simulation for the in game day
        self.RunGameLoop()

    def RunGameLoop(self):
        while self.inGameTime < self.maxTime:
            #Generate a log and see if it results
            #in new incident(s) to deal with
            #If it does, add it to the queue of incidents

            try:
                incident = response(self.inGameTime)
                print(incident)
            except:
                pass #Do Nothing

            #Increment the time
            self.inGameTime += 1


        print(f"Day {self.day} done")
        self.day += 1


    def TravelCost(self, startNode: int, endNode: int) -> int:
        return dijkstraPath(self.graphDict, startNode, endNode)
        
    