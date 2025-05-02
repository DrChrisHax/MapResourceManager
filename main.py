#Entry point for the program

from simulation.SimulationEngine import SimulationEngine
from ui.gui import SimulationUI

def main():
    engine = SimulationEngine()
    engine.run()

if __name__ == "__main__":
    main()