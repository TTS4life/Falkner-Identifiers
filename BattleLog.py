#!/usr/bin/python3

import pandas as pd
from copy import deepcopy


class BattleLog:
	def __init__(self):
		self.log = []
		self.seed = 0
		self.win = None
		self.battle = 0

		
		# = pd.DataFrame([
		# 	["Ember", 9, "", "", "Tackle", 4, "crit", "Ember", 5, "", "Burn", "",],
		# 	["Ember", 14, "crit", "", "Tackle", 2, "crit"]
		# ])
	
	def append(self, turn):
		if(self.battle == 0):
			self.log[0] += turn
		else:
			self.log[self.battle - 1] += turn

	def write_output(self, file):
		pd.DataFrame(self.log).to_csv(file)

	def mark_outcome(self, victory):
		if self.battle == 0:
			self.log[self.battle].append(victory)
		else:
			self.log[self.battle- 1].append(victory)

		self.battle += 1
		self.log.append([])

	def start_battle(self, seed):
		print("Starting battle ", self.battle, " ", hex(seed))
		if self.battle == 0:
			self.log.append([hex(seed)])
		else:
			self.log[self.battle - 1].append(hex(seed))


log = BattleLog()

class BattleTurn:
	def __init__(self):
		self.cynda_hp = 0
		self.cynda_action = ""
		self.cynda_roll = 0
		self.cynda_burn = 0
		self.cynda_crit = 0

		self.opponent_action = ""
		self.opponent_roll = 0
		self.opponent_crit = 0
		self.opponent_hp = 0
		self.turn_count = 0	

	# def __del__(self):
	# 	self.commitTurn()

	def to_array(self):
		return [self.turn_count, self.cynda_hp, self.cynda_action, self.cynda_roll, self.cynda_burn, self.cynda_crit,
					   		self.opponent_action, self.opponent_roll, self.opponent_crit, self.opponent_hp]

	def commitTurn(self):
		log.append(self.to_array())
		
	def print(self):
		print(self.to_array())
		


def debug():
	log = BattleLog()
	log.df.to_csv("out.txt")

if __name__ == '__main__':
	debug()