
from algorithms.analyzeIncident import response

class SimulationEngine:
    def __init__(self):
        self.inGameTime = 0 #In game minutes
        self.maxTime = 12 * 60 #12 hours per simulated day
        self.day = 1

        self.resources = {
            'police': [],
            'fire': [],
            'medical': []
        }

        #TODO: Uncomment after implemented by Adam and Daniel
        #self.map = Map()
        #self.logginSystem = LogginSystem()

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

            #Run some code to deal with the incidents
            #self.ScheduleIncidents()

            #Tell the map about the locations of all the vehicles

            #Increment the time
            self.inGameTime += 1

            #Tell the map to update its time

        print(f"Day {self.day} done")
        self.day += 1

            

    def ScheduleIncidents(self):
        print("Not Implemented Yet")
