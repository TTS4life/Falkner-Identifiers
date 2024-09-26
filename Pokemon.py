from copy import deepcopy
import math

class Pokemon:
	def __init__(self, base_stats, level, species = 0, actual_hp = None):
		self.base_stats = base_stats
		self.species = species
		self.stage = deepcopy([0,0,0,0,0,0,0,0])
		self.actual = deepcopy(self.base_stats)
		if actual_hp != None:
			self.actual[0] = actual_hp
		self.actual = getModifiedStats(self.base_stats,self.stage,self.actual[0])
		self.stealth_rock_onField = False
		self.burnt = False
		self.turn1 = True
		self.level = level
		self.pumped = False
		self.attracted = False
		self.flinch = False


	#currently, weather, screen, targets, weather, flash fire, item, me first, type 2, super effectiveness-reducing ability, expert belt, tented lens, type reducing berries
	# movePower is passed in as int, burnt is passed in as bool, crit is passed in as multiplier, dmgRand is passed in before /100, effectiveness is multiplier, dmgType is physical/spec, stab is multiplier
	def attack(self, enemy, movePower, burnt, crit, dmgRand, effectiveness, dmgType, stab, metronome = 0):
		if burnt and dmgType == "physical":
			burnt = 0.5
		else:
			burnt = 1
		if dmgType == "physical":
			atk = self.actual[1]
			defense = enemy.actual[2]
			if crit == 2:
				if enemy.stage[2] > 0:
					defense = enemy.base_def
				if self.stage[1] < 0:
					atk = self.base_atk
		else:
			atk = self.actual[3]
			defense = enemy.actual[4]
			if crit == 2:
				if enemy.stage[4] > 0:
					defense = enemy.base_spdef
				if self.stage[3] < 0:
					atk = self.base_spatk
		
		#print(f"MovePower: {movePower}, dmgRand: {dmgRand-85}, enemy def: {defense}")
		
		damage = int(int(int(int(int(int(int(int((int(2 * self.level / 5) + 2) * movePower * atk / defense) / 50) * burnt) + 2) * crit * (metronome+10)/10) * dmgRand / 100) * stab) * effectiveness)
		enemy.actual[0] -= damage
		if enemy.actual[0] < 0:
			enemy.actual[0] = 0
		return damage
	
	def tackle(self, enemy, rng):
		rng.advance(5)
		crit = [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1][rng.getRand() % 16] # crit if %16 = 0
		rng.advance()
		dmgRand = [100, 99, 98, 97, 96, 95, 94, 93, 92, 91, 90, 89, 88, 87, 86, 85][rng.getRand() % 16]
		rng.advance()
		accCheck = (rng.getRand()%100) + 1 # miss if check > acc
		accStage = self.stage[7] - enemy.stage[6]
		if accStage >= 6:
			accStage = 6
		elif accStage <= -6:
			accStage = -6
		adjustedAccuracy = int(math.floor(95 * ([33, 36, 43, 50, 60, 75, 100, 133, 166, 200, 250, 266, 300] [accStage+6] / 100)))
		if accCheck > adjustedAccuracy:
			rng.jump(rng.frame-2)
			return f"{self.species} Tackle Miss", 0
		else:
			#def attack(self, enemy, movePower, burnt, crit, dmgRand, effectiveness, dmgType, stab):
			damage = self.attack(enemy, 35, self.burnt, crit, dmgRand, 1, "physical", 1.5)
			if crit == 2:
				return f"{self.species} Tackle Crit", damage
			return f"{self.species} Tackle", damage
	
	def attack_simulation(self, enemy, movePower, burnt, effectiveness, dmgType, stab):
		if burnt and dmgType == "physical":
			burnt = 0.5
		else:
			burnt = 1
		if dmgType == "physical":
			atk = self.actual[1]
			defense = enemy.actual[2]
		else:
			atk = self.actual[3]
			defense = enemy.actual[4]
		#print(self.level, movePower, atk, defense, burnt, stab, effectiveness, self.actual, enemy.actual)
		damage = int(int(int((int(int(int((int(2 * self.level / 5) + 2) * movePower * atk / defense) / 50) * burnt) + 2)) * stab) * effectiveness)
		return damage
	
	def updateStats(self):
		#print(f"Need to udpate stats! Base: {self.base_stats}")
		self.actual = getModifiedStats(self.base_stats, self.stage, self.actual[0])

	def reset(self):
		self.stage = deepcopy([0,0,0,0,0,0,0,0])
		self.actual = deepcopy(getModifiedStats(self.base_stats,self.stage, self.base_stats[0]))
		self.actual[0] = deepcopy(self.base_stats[0])
		self.stealth_rock_onField = False
		self.burnt = False
		self.turn1 = True
		self.attracted = False

	def reset_flinch_flag(self):
		self.flinch = False


class Cyndaquil(Pokemon):

	def decide(self, enemy, rng):
		if enemy.species == "pidgey":
			return "ember"
		else:
			if enemy.actual[0] < 20:
				return "ember"
			else:
				if self.actual[0] <= 10:
					return "pot"
				else:
					return "ember"

	def useMove(self, move, enemy, rng):
			damage = 0
			res = ""
			if move == "ember":
				res, damage = self.ember(enemy, rng)
			elif move == "pot":
				res. damage = self.potion(enemy, rng)
			elif move == "ball":
				res, damage = self.ball(enemy, rng)
			elif move == "tackle":
				res, damage = self.tackle(enemy, rng)
			elif move == "leer":
				res, damage = self.leer(enemy, rng)
			elif move == "qa":
				res, damage = self.qa(enemy, rng)
			return res, damage
		
	def ember(self, enemy, rng):
		rng.advance(4)
		rng.advance()
		if self.pumped:
			crit = [2,1,1,1][rng.getRand() % 4]
		else:
			crit = [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1][rng.getRand() % 16]
		rng.advance()
		dmgRand = [100, 99, 98, 97, 96, 95, 94, 93, 92, 91, 90, 89, 88, 87, 86, 85][rng.getRand() % 16]
		rng.advance()
		accCheck = (rng.getRand()%100) + 1 # miss if check > acc
		accStage = self.stage[7] - enemy.stage[6]
		if accStage >= 6:
			accStage = 6
		elif accStage <= -6:
			accStage = -6
		adjustedAccuracy = int(math.floor(100 * ([33, 36, 43, 50, 60, 75, 100, 133, 166, 200, 250, 266, 300] [accStage+6] / 100)))
		if accCheck > adjustedAccuracy:
			rng.jump(rng.frame-2)
			return "Ember Miss", 0, False
		else:
			#def attack(self, enemy, movePower, burnt, crit, dmgRand, effectiveness, dmgType, stab):
			#print(f"base hp: {self.base_stats[0]}")
			if int(self.base_stats[0] / 3) >= self.actual[0]:
				movePower = 60
			else:
				movePower = 40
			damage = self.attack(enemy, movePower, self.burnt, crit, dmgRand, 1, "special", 1.5)
			#flinch check, although useless when enemy is faster
			rng.advance()
			burnCheck = rng.getRand() % 100
			if (burnCheck < 10) and (not enemy.burnt) :
				enemy.burnt = True
				if crit == 2:
					return f"Ember crit burn", damage
				else:
					return f"Ember burn", damage
			if crit == 2:
				return f"Ember crit", damage
			return f"Ember", damage

	def levelUp(self):
		if self.level == 13:
			return # Not meant to lvl up
		
		self.base_stats = [33, 22, 18, 26, 16, 26]
		self.level = 13
		self.actual[0] += 2
		self.updateStats()
		
	def leer(self, enemy, rng):
		rng.advance(4)
		rng.advance()
		accCheck = (rng.getRand()%100) + 1 # miss if check > acc
		accStage = self.stage[7] - enemy.stage[6]
		if accStage >= 6:
			accStage = 6
		elif accStage <= -6:
			accStage = -6
		adjustedAccuracy = int(math.floor(100 * ([33, 36, 43, 50, 60, 75, 100, 133, 166, 200, 250, 266, 300] [accStage+6] / 100)))
		if accCheck > adjustedAccuracy:
			rng.jump(rng.frame-2)
			return "Leer Miss", 0
		else:
			#print(f"trying leer, {enemy.actual[0]}")
			enemy.stage[2] -= 1
			if enemy.stage[2] < -6:
				enemy.stage[2] = -6
			enemy.updateStats()
			#print(f"I am at {self.stage[2]} | {self.actual[0]}, Enemy is at {enemy.stage[2]} | {enemy.actual[0]}")
			return f"Leer", 0
	
	def smokescreen(self, enemy, rng):
		rng.advance(4)
		rng.advance()
		accCheck = (rng.getRand()%100) + 1 # miss if check > acc
		accStage = self.stage[7] - enemy.stage[6]
		if accStage >= 6:
			accStage = 6
		elif accStage <= -6:
			accStage = -6
		adjustedAccuracy = int(math.floor(100 * ([33, 36, 43, 50, 60, 75, 100, 133, 166, 200, 250, 266, 300] [accStage+6] / 100)))
		if accCheck > adjustedAccuracy:
			rng.jump(rng.frame-2)
			return "Smokescreen Miss"
		else:
			#print(f"trying leer, {enemy.actual[0]}")
			enemy.stage[7] -= 1
			if enemy.stage[7] < -6:
				enemy.stage[7] = -6
			enemy.updateStats()
			#print(f"I am at {self.stage[2]} | {self.actual[0]}, Enemy is at {enemy.stage[2]} | {enemy.actual[0]}")
			return f"Smokescreen"
	
	def potion(self, enemy, rng, health = 20):
		rng.advance(2)
		self.actual[0] += health
		if self.actual[0] > self.base_stats[0]:
			self.actual[0] = self.base_stats[0]
		return f"Potion to {self.actual[0]}"
	
	def ball(self, enemy, rng):
		rng.advance(2)
		return f"Ball"
	
	def qa(self, enemy, rng):
		rng.advance(5)
		crit = [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1][rng.getRand() % 16] # crit if %16 = 0
		rng.advance()
		dmgRand = [100, 99, 98, 97, 96, 95, 94, 93, 92, 91, 90, 89, 88, 87, 86, 85][rng.getRand() % 16]
		rng.advance()
		accCheck = (rng.getRand()%100) + 1 # miss if check > acc
		accStage = self.stage[7] - enemy.stage[6]
		if accStage >= 6:
			accStage = 6
		elif accStage <= -6:
			accStage = -6
		adjustedAccuracy = int(math.floor(100 * ([33, 36, 43, 50, 60, 75, 100, 133, 166, 200, 250, 266, 300] [accStage+6] / 100)))
		if accCheck > adjustedAccuracy:
			rng.jump(rng.frame-2)
			return f"{self.species} QA Miss", 0
		else:
			#def attack(self, enemy, movePower, burnt, crit, dmgRand, effectiveness, dmgType, stab):
			damage = self.attack(enemy, 40, self.burnt, crit, dmgRand, 1, "physical", 1.5)
			if crit == 2:
				return f"{self.species} QA Crit", damage
			return f"{self.species} QA", damage
	
	def reset(self, init_hp = None):
		self.stage = [0,0,0,0,0,0,0,0]
		self.base_stats = deepcopy(cynda_lv12)
		self.level = 12
		self.actual = getModifiedStats(self.base_stats,self.stage,self.base_stats[0])
		self.actual[0] = self.base_stats[0]
		self.stealth_rock_onField = False
		self.burnt = False
		self.turn1 = True
		self.attracted = False
		self.pumped = False
		if init_hp != None:
			self.actual[0] = init_hp
		self.lastMove = None
		self.metronome = 0
		self.flinch = False

class Pidgey(Pokemon):
	def decide(self, enemy, rng):
		#stomp_maxroll = self.attack_simulation(enemy,65,self.burnt,1,physical,1.5)
		tackle_max = self.attack_simulation(enemy, 35, self.burnt, 1, "physical", 1.5)
		if enemy.actual[0] <= tackle_max:
			move_choices = ["tackle"]
		else:
			move_choices = ["tackle", "sand"]
		rng.advance(6)
		#Falkner don't have potion
		rng.advance(5)
		call = rng.getRand()
		return move_choices[call%len(move_choices)]

	def useMove(self, move, enemy, rng):
		if move == "tackle":
			res = self.tackle(enemy, rng)
		elif move == "sand":
			res = self.sand(enemy, rng)
		else:
			print(f"{move} is not available")
		return res
	
	def sand(self, enemy, rng):
		rng.advance(4)
		rng.advance()
		accCheck = (rng.getRand()%100) + 1 # miss if check > acc
		accStage = self.stage[7] - enemy.stage[6]
		if accStage >= 6:
			accStage = 6
		elif accStage <= -6:
			accStage = -6
		adjustedAccuracy = int(math.floor(100 * ([33, 36, 43, 50, 60, 75, 100, 133, 166, 200, 250, 266, 300] [accStage+6] / 100)))
		if accCheck > adjustedAccuracy:
			rng.jump(rng.frame-2)
			return "Sand Attack Miss", 0
		else:
			#print(f"trying leer, {enemy.actual[0]}")
			enemy.stage[7] -= 1
			if enemy.stage[7] < -6:
				enemy.stage[7] = -6
			enemy.updateStats()
			#print(f"I am at {self.stage[2]} | {self.actual[0]}, Enemy is at {enemy.stage[2]} | {enemy.actual[0]}")
			return f"Sand Attack", 0

class Pidgeotto(Pokemon):
	def decide(self, enemy, rng):
		extra = False
		#stomp_maxroll = self.attack_simulation(enemy,65,self.burnt,1,physical,1.5)
		tackle_max = self.attack_simulation(enemy, 35, self.burnt, 1, "physical", 1.5)
		gust_max = self.attack_simulation(enemy, 40, self.burnt, 1, "special", 1.5)
		if enemy.actual[0] <= tackle_max:
			move_choices = ["tackle", "gust"]
		elif enemy.actual[0] <= gust_max:
			move_choices = ["gust"]
		else:
			if self.actual[0] < self.base_stats[0]:
				move_choices = ["roost", "gust"]
			else:
				move_choices = ["gust"]

		rng.advance(6)
		
		rng.advance(5)
		call = rng.getRand()
		return move_choices[call%len(move_choices)]

	def useMove(self, move, enemy, rng):
		damage = 0
		if move == "tackle":
			res, damage = self.tackle(enemy, rng)
		elif move == "gust":
			res, damage = self.gust(enemy, rng)
		elif move == "roost":
			res = self.roost(enemy, rng)
		return res, damage
	
	def gust(self, enemy, rng):
		rng.advance(5)
		crit = [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1][rng.getRand() % 16] # crit if %16 = 0
		rng.advance()
		dmgRand = [100, 99, 98, 97, 96, 95, 94, 93, 92, 91, 90, 89, 88, 87, 86, 85][rng.getRand() % 16]
		rng.advance()
		accCheck = (rng.getRand()%100) + 1 # miss if check > acc
		accStage = self.stage[7] - enemy.stage[6]
		if accStage >= 6:
			accStage = 6
		elif accStage <= -6:
			accStage = -6
		adjustedAccuracy = int(math.floor(100 * ([33, 36, 43, 50, 60, 75, 100, 133, 166, 200, 250, 266, 300] [accStage+6] / 100)))
		if accCheck > adjustedAccuracy:
			rng.jump(rng.frame-2)
			return "Gust Miss", 0
		else:
			#def attack(self, enemy, movePower, burnt, crit, dmgRand, effectiveness, dmgType, stab):
			damage = self.attack(enemy, 40, self.burnt, crit, dmgRand, 1, "special", 1.5)
			if crit == 2:
				return f"Gust Crit", damage
			return f"Gust", damage
	
	def roost(self, enemy, rng):
		rng.advance(4)
		self.actual[0] += 20
		if self.actual[0] > self.base_stats[0]:
			self.actual[0] = self.base_stats[0]
		return "Roost"


def getModifiedStats(base_stats, stage, current_hp):
	#print(f"before adjustment: {base_stats}")
	res = deepcopy(base_stats)
	res[0] = current_hp
	for x in range(1,6):
		if stage[x] == 0:
			continue
		elif stage[x] > 0:
			res[x] = int(math.floor(res[x] * ((2+stage[x])/2)))
		else:
			res[x] = int(math.floor(res[x] * (2/(2-stage[x]))))
	#print(f"Adjusted to {res}")
	return res
