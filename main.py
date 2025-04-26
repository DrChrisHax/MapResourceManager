#Entry point for the program

from simulation.SimulationEngine import SimulationEngine


def main():
    
    engine = SimulationEngine()
    engine.Start() #Later have a start button in the UI that starts this



if __name__ == "__main__":
    main()