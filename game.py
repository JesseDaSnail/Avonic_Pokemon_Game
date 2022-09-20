import numpy as np
import pandas as pd
from tabulate import tabulate
import time

class PokemonGame:
    def __init__(self):
        self.poke1 = None
        self.poke2 = None
        self.pokemon_stats = pd.read_csv("pokemon_stats.csv")
        self.pokemon_moves = pd.read_csv("pokemon_moves.csv")
        self.pokemon_types = pd.read_csv("pokemon_types.csv").set_index("Attacking")
        self.chosen_move = None
    
    def display_start_menu(self):
        """
        Displays the start menu and asks for the user to chose a pokemon.
        """

        welcome_text = """
--------------------------------------------------------------------------------------------------------------
                       Welcome to the Avonic intake pokemon game!
                       To start a battle, pick one of the following pokemon.
--------------------------------------------------------------------------------------------------------------
                       """
        print(welcome_text)
        print(self.pokemon_stats)
        print("-"*110)

        choice = None
        while choice not in range(0,self.pokemon_stats.shape[0]):
            try:
                choice = int(input(f"Choose pokemon (0-{self.pokemon_stats.shape[0]-1}): "))
            except ValueError:
                print(f"Please input an integer between 0 and {self.pokemon_stats.shape[0]-1}")
            
        self.poke1 = self.pokemon_stats.iloc[choice].to_dict()
        print(f"You have chosen {self.poke1['name']}!")

        # self.poke2 = self.pokemon_stats.iloc[np.random.randint(0,4)].to_dict()
        choice = None
        while choice not in range(0,self.pokemon_stats.shape[0]):
            try:
                choice = int(input(f"Choose enemy pokemon (0-{self.pokemon_stats.shape[0]-1}): "))
            except ValueError:
                print(f"Please input an integer between 0 and {self.pokemon_stats.shape[0]-1}")

        self.poke2 = self.pokemon_stats.iloc[choice].to_dict()
        print(f"Your opponent has chosen {self.poke2['name']}!")


    def display_turn(self):
        """
        Displays the current game state and asks the user for a choice of move.
        """

        screen_text = f"""
Enemy {self.poke2['name']}: {self.poke2['health']}

Your {self.poke1['name']}: {self.poke1['health']}
-------------------------------------------------------
What will you do?

1: {self.poke1["move1"]}
2: {self.poke1["move2"]}
3: {self.poke1["move3"]}
4: {self.poke1["move4"]}

"""
        output = tabulate([[screen_text]], tablefmt='grid')
        print(output)

        choice = None
        while choice not in range(1,5):
            try:
                choice = int(input("Choose next move (1-4): "))
            except ValueError:
                print("Please input an integer!")
        self.chosen_move = self.poke1[f'move{choice}']
  

    def player_move(self):
        """
        Handles the player's chosen move
        """

        move = self.chosen_move
        print(f"Your {self.poke1['name']} used {move}!")
        time.sleep(1)
        
        move_series = self.pokemon_moves.loc[self.pokemon_moves['name'] == move]

        if move_series['message'].item() != 'default':
            print(move_series['message'].item())
            time.sleep(1)

        if float(move_series['power']) > 0:
            # calculate damage
            type_multiplier = self.pokemon_types[self.poke2['type']][move_series['type'].item()]
            if type_multiplier > 1:
                print("It's super effective!")
            elif type_multiplier < 1:
                print("It's not very effective!")

            attack_defense_multiplier = self.poke1['attack'] / self.poke2['defense']
            damage = float(move_series['power']) * attack_defense_multiplier * type_multiplier
            if int(move_series['multihit']):
                num_hits = np.random.randint(1,6)
                damage *= num_hits
                print(f"Hit {num_hits} times!")
            self.poke2['health'] -= damage
            print(f"Damage done = {damage}")
            time.sleep(1)

        if float(move_series['attackboost']) > 0:
            self.poke1['attack'] *= int(move_series['attackboost'])
            print(f"Your {self.poke1['name']}'s attack was {(float(move_series['attackboost'])>1)*'increased'}{(float(move_series['attackboost'])<1)*'decreased'}!")
            time.sleep(1)

        if float(move_series['speedboost']) > 0:
            self.poke1['speed'] *= int(move_series['speedboost'])
            print(f"Your {self.poke1['name']}'s speed was {(float(move_series['speedboost'])>1)*'increased'}{(float(move_series['speedboost'])<1)*'decreased'}!")
            time.sleep(1)

        if self.poke2['health'] <= 0:
            print(f"Enemy {self.poke2['name']} has fainted!")
            return 1


    def enemy_move(self):
        """
        Handles the enemy's randomly chosen move
        """

        random_choice = np.random.randint(0,4)
        move = self.poke2[f'move{random_choice+1}']
        print(f"Enemy {self.poke2['name']} used {move}!")
        time.sleep(1)
        
        move_series = self.pokemon_moves.loc[self.pokemon_moves['name'] == move]
        if float(move_series['power']) > 0:
            # calculate damage
            type_multiplier = self.pokemon_types[self.poke1['type']][move_series['type'].item()]
            if type_multiplier > 1:
                print("It's super effective!")
            elif type_multiplier < 1:
                print("It's not very effective!")
            
            attack_defense_multiplier = self.poke2['attack'] / self.poke1['defense']
            damage = float(move_series['power']) * attack_defense_multiplier * type_multiplier
            if int(move_series['multihit']):
                num_hits = np.random.randint(1,6)
                damage *= num_hits
                print(f"Hit {num_hits} times!")
            self.poke1['health'] -= damage
            print(f"Damage done = {damage}")
            time.sleep(1)

        if float(move_series['attackboost']) > 0:
            self.poke2['attack'] *= int(move_series['attackboost'])
            print(f"Enemy {self.poke2['name']}'s attack was {(float(move_series['attackboost'])>1)*'increased'}{(float(move_series['attackboost'])<1)*'decreased'}!")
            time.sleep(1)

        if float(move_series['speedboost']) > 0:
            self.poke2['speed'] *= float(move_series['speedboost'])
            print(f"Enemy {self.poke2['name']}'s speed was {(float(move_series['speedboost'])>1)*'increased'}{(float(move_series['speedboost'])<1)*'decreased'}!")
            time.sleep(1)

        if self.poke1['health'] <= 0:
            print(f"Your {self.poke1['name']} has fainted!")
            return 2


    def run(self):
        """
        Main loop
        """

        while True:
            self.display_turn()
            if self.poke1["speed"] > self.poke2["speed"]:
                exit_condition = self.player_move()
                if exit_condition:
                    break
                exit_condition = self.enemy_move()
                if exit_condition:
                    break
            else:
                exit_condition = self.enemy_move()
                if exit_condition:
                    break
                exit_condition = self.player_move()
                if exit_condition:
                    break
        self.end_screen(exit_condition)
    

    def end_screen(self,win_condition):
        if win_condition == 1:
            screen_text = f"""
Victory!
You have won the game!
Congrats!
"""
            output = tabulate([[screen_text]], tablefmt='grid')
            print(output)
        else:
            screen_text = f"""
Defeat!
You have lossed the game!
Better luck next time!
"""
            output = tabulate([[screen_text]], tablefmt='grid')
            print(output)