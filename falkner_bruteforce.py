#!/usr/bin/python3

from Pokemon import Cyndaquil, Pidgeotto, Pidgey
from RNG import RNG
from copy import deepcopy
from BattleState import BattleState

# pidgeotto_burned = False
# pidgeotto_current_hp = 28

# cynda_current_hp = 18


actions = ["ember",  "tackle", "leer", "qa", "pot", "ball"  ]

winning_combos = []
all_combos = []

num_combos = 20 # how many of the best win cons to show


def main(seed, turn):
	cynda = Cyndaquil(deepcopy([31, 20, 17, 24, 15, 24]), 12, 31)

	pidgeotto = Pidgeotto(deepcopy([40, 21, 20, 18, 18, 14]), 13, species = "pidgeotto")
	pidgey = Pidgey(deepcopy([26, 14, 10, 11, 11, 15]), 9, species = "pidgey")

	# pidgeotto.actual[0] = pidgeotto_current_hp
	# pidgeotto.burnt = pidgeotto_burned

	state = BattleState(seed, 0, cynda, pidgeotto, pidgey)

	for i in range(turn):
		if(state.cyndaquil.actual[0] < 11 ):
			state.do_action('pot')
		else:	
			state.do_action('ember')	#Advance up to identifier

	print(f"Winning combos for seed {hex(state.rng.seed)}")

	#Recursion begin!
	for action in actions:
		next_turn(deepcopy(state), action, 1)

	winning_combos.sort(key=len)

	if(len(winning_combos) > 0):
		for i in range(min(num_combos, len(winning_combos))):
			print((len(winning_combos[i]) - 1) / 2, winning_combos[i])


def next_turn(state, action, turn_count):
	state.do_action(action)
	#Pidgeotto died, base case 1

	all_combos.append(deepcopy(state.actions))

	if state.cyndaquil.actual[0] > 0 and not state.all_enemies_dead() and turn_count <= 5:
		for next_action in actions:
				next_turn(deepcopy(state), next_action, turn_count + 1)
	
	if state.all_enemies_dead():
		state.actions.append(state.cyndaquil.actual[0])
		winning_combos.append(deepcopy(state.actions))
		return
	
	#Cynda died, base case 2
	elif state.cyndaquil.actual[0] <= 0 and not state.all_enemies_dead():
		return 
	
	elif state.cyndaquil.actual[0] <= 0 and state.all_enemies_dead():
		return #cooked case

def debug():
	seed = 0x560b1c43
	actions = ['ember', 'ember', 'ember', 'ember', 'ember']
	cynda = Cyndaquil(deepcopy([31, 20, 17, 24, 15, 24]), 12, 31)

	pidgeotto = Pidgeotto(deepcopy([40, 21, 20, 18, 18, 14]), 13, species = "pidgeotto")
	pidgey = Pidgey(deepcopy([26, 14, 10, 11, 11, 15]), 9, species = "pidgey")

	state = BattleState(seed, 0, cynda, pidgeotto, pidgey)

	for action in actions:
		state.do_action(action)
		print(state.rng.frame)
	
	print(state.actions)
	

if __name__ == '__main__':
	# debug()
	# exit()

	seed = int( input("What seed? "), 16)
	turn = int(input("What turn? "))
	
	main(seed, turn)