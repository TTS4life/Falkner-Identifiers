from RNG import RNG


class BattleState:
	def __init__(self, rng, adv, cynda, pidgeotto, pidgey):
		self.rng = RNG(rng)
		self.cyndaquil = cynda
		self.active_pokemon = [ pidgey, pidgeotto ]
		self.actions = []

		for _ in range(adv):
			self.rng.jump(adv)
	
	def get_enemy_poke(self):
		if len(self.active_pokemon) == 0:
			return None
		return self.active_pokemon[0]
	
	
	def enemy_fainted_check(self):
		if self.get_enemy_poke().actual[0] <= 0:
			self.active_pokemon.pop(0)
			self.cyndaquil.levelUp()
			self.rng.jump(self.rng.frame -1)
			return True
		return False
	
	def all_enemies_dead(self):
		return len(self.active_pokemon) == 0

	def do_action(self, action):

		if(self.all_enemies_dead() or self.cyndaquil.actual[0] <= 0):
			return
		
		falk_act = ""
		dmg = 0
		en_dmg = 0
		
		#Falkner think
		falk_decision = self.get_enemy_poke().decide(self.cyndaquil, self.rng)

		# self.actions.append(self.rng.frame)

		#cyndaquil attack
		action, dmg = self.cyndaquil.useMove(action, self.get_enemy_poke(), self.rng)

		# self.actions.append(self.get_enemy_poke().actual[0])

		#Falkner attack
		if self.get_enemy_poke().actual[0] > 0:
			falk_act, en_dmg = self.get_enemy_poke().useMove(falk_decision, self.cyndaquil, self.rng)


		if self.cyndaquil.actual[0] <= 0:
			self.cyndaquil.actual[0] = 0

		#Handle burn
		if self.get_enemy_poke().burnt == True and self.cyndaquil.actual[0] > 0:
			self.get_enemy_poke().actual[0] -= int(self.get_enemy_poke().base_stats[0] / 8)

		# print(f"End turn: {self.get_enemy_poke().species} has {self.get_enemy_poke().actual[0]}, cynda has {self.cyndaquil.actual[0]}")

		self.enemy_fainted_check()

		self.actions.append([self.cyndaquil.actual[0], action, dmg])
		self.actions.append([0 if self.get_enemy_poke() is None else self.get_enemy_poke().actual[0], falk_act, en_dmg])

	
		# self.actions.append(self.cyndaquil.actual[0])

