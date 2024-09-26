#!/usr/bin/python3

from Pokemon import Cyndaquil, Pidgeotto, Pidgey
from RNG import RNG
from copy import deepcopy

pidgeotto_burned = False
pidgeotto_current_hp = 28

cynda_current_hp = 18

battle_rng_advances = 90
battle_rng_seed = 0x560b1c99

actions = ["ember",  "tackle", "qa", "pot", "ball", "leer" ]

winning_combos = []


class BattleState:
	def __init__(self, rng, adv, cynda, pidgeotto):
		self.rng = RNG(rng)
		self.cyndaquil = cynda
		self.pidgeotto = pidgeotto
		self.actions = []

		for _ in range(adv):
			self.rng.jump(adv)

	def do_action(self, action):
		skip_cynda_attack = 0
		falk_act = ""
		dmg = 0
		
		#Falkner think
		falk_decision = self.pidgeotto.decide(self.cyndaquil, self.rng)


		# self.actions.append(self.rng.frame)

		if action == "ball":
			self.cyndaquil.potion(None, self.rng, 0)
			skip_cynda_attack = 1

		if action == "pot":
			self.cyndaquil.potion(None, self.rng)
			skip_cynda_attack = 1

		#cyndaquil attack
		if skip_cynda_attack == 0:
			self.cyndaquil.useMove(action, self.pidgeotto, self.rng)


		#Falkner attack
		if self.pidgeotto.actual[0] > 0:
			# self.actions.append(falk_decision)
			falk_act, dmg = self.pidgeotto.useMove(falk_decision, self.cyndaquil, self.rng)


		#Handle burn
		if self.pidgeotto.burnt == True:
			self.pidgeotto.actual[0] -= int(self.pidgeotto.base_stats[0] / 8)

		# print(f"End turn: Pidgeotto has {self.pidgeotto.actual[0]}, cynda as {self.cyndaquil.actual[0]}")

		self.actions.append(action)
		self.actions.append([falk_act, dmg])
		# self.actions.append(self.cyndaquil.actual[0])




def main():
	cynda = Cyndaquil(deepcopy([31, 20, 17, 24, 15, 24]), 12, 31)
	cynda.levelUp()

	cynda.actual[0] = cynda_current_hp

	pidgeotto = Pidgeotto(deepcopy([40, 21, 20, 18, 18, 14]), 13, species = "pidgeotto")

	pidgeotto.actual[0] = pidgeotto_current_hp
	pidgeotto.burnt = pidgeotto_burned

	state = BattleState(battle_rng_seed, battle_rng_advances, cynda, pidgeotto)

	print(f"Winning combos for seed {hex(state.rng.seed)}")

	#Recursion begin!
	for action in actions:
		next_turn(deepcopy(state), action, 1)

	print(winning_combos.sort(key=len))

	for combo in winning_combos:
		print(combo)


def next_turn(state, action, turn_count):
	
	state.do_action(action)
	#Pidgeotto died, base case 1
	if state.pidgeotto.actual[0] <= 0 and state.cyndaquil.actual[0] > 0:
		state.actions.append(state.cyndaquil.actual[0])
		winning_combos.append(deepcopy(state.actions))
		return
	#Cynda died, base case 2
	elif state.cyndaquil.actual[0] <= 0 and state.pidgeotto.actual[0] > 0:
		# print("Lose con found")
		return state.actions.append("Cynda died")
	elif state.cyndaquil.actual[0] <= 0 and state.pidgeotto.actual[0] > 0:
		return #cooked case
	elif turn_count >= 5:
		#Too many turns have passed, stop
		# print("Exceeded turns")
		return 
	else:
		for action in actions:
			next_turn(deepcopy(state), action, turn_count + 1)

		#return ERR, could not find wincon or bad base case


def debug():
	cynda = Cyndaquil(deepcopy([31, 20, 17, 24, 15, 24]), 12, 31)
	cynda.levelUp()

	cynda.actual[0] = cynda_current_hp

	pidgeotto = Pidgeotto(deepcopy([40, 21, 20, 18, 18, 14]), 13, species = "pidgeotto")

	pidgeotto.actual[0] = pidgeotto_current_hp
	pidgeotto.burnt = pidgeotto_burned

	state = BattleState(battle_rng_seed, battle_rng_advances, cynda, pidgeotto)

	for action in ["leer", "ember", "ember"]:
		state.do_action(action)
		print("cynda hp ", state.cyndaquil.actual[0])
		# print(state.pidgeotto.actual[0])

	print(state.actions)

if __name__ == '__main__':
	main()