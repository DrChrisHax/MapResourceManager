#Entry point for the program

from simulation.SimulationEngine import SimulationEngine
from ui.gui import SimulationUI

def main():
    
    engine = SimulationEngine()
    engine.Start() #Later have a start button in the UI that starts this

    # Create the UI and pass the engine to it later if needed
    app = SimulationUI()
    app.run()


if __name__ == "__main__":
    main()