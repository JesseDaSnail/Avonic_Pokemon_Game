import numpy as np
import pandas as pd
from game import PokemonGame

def main():
    current_game = PokemonGame()
    current_game.display_start_menu()
    current_game.run()


if __name__ == "__main__":
    main()
