#Entry point for the program

from simulation.SimulationEngine import SimulationEngine
from ui.gui import SimulationUI

def main():
    engine = SimulationEngine()
    app = SimulationUI(engine)
    app.run()


if __name__ == "__main__":
    main()