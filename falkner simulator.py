#!/usr/bin/python3


import math
from itertools import product
from copy import deepcopy
import datetime
from RNG import RNG
from Pokemon import Cyndaquil, Pidgey, Pidgeotto
from BattleLog import BattleTurn, log

tackle = "tackle"
leer = "leer"
ember = "ember"
smokescreen = "smokescreen"
sand = "sand"
qa = "qa"

pot = "pot"
ball = "ball"

gust = "gust"
roost = "roost"

physical = "physical"
special = "special"




pidgey_stats = [26, 14, 10, 11, 11, 15]
pidgeotto_stats = [40, 21, 20, 18, 18, 14]

piplup_possible_actions = [pot, ball, ember, qa, tackle, smokescreen]

cynda = 0
pidgey = 1
pidgeotto = 2



###########################################
debug_mode = False
debug_seed = 0x560ada68
debug_moves = [ember, ember, ember, ember, ember, ember, ember, ember, ember, ember]


cynda_hp = 31

cluster = 0

statistic = False


falkner_potion = [False, False]


###########################################


def getCluster(n):
    clusters = [80, 86, 33, 38, 44, 49, 55, 61, 66, 72, 78, 83, 89, 35, 41, 47, 52, 58, 64, 69, 75, 80]
    delay_center = 0x1226c - 152*12
    upper = clusters[n]*0x1000000 + 0xa0000

    delay_center += n*152*2
    mid = upper+delay_center
    while True:
        seed = RNG(mid)
        frame = seed.jump(11)
        if seed.getRand()%2 == 1:
            break
        mid -= 1

    upper_bound = mid+1

    mid = upper+delay_center
    while True:
        seed = RNG(mid)
        frame = seed.jump(11)
        if seed.getRand()%2 == 1:
            break
        mid += 1

    lower_bound = mid-1
    clusterN = []
    for seed in range(upper_bound,lower_bound+1):
        clusterN.append(seed)
    print(f"{hex(upper_bound)} ~ {hex(lower_bound)}")
    return clusterN

def debug():

    battle_res = []

    battleRNG = RNG(debug_seed)
    cynda = Cyndaquil(deepcopy([31, 20, 17, 24, 15, 24]),12,cynda_hp)

    pidgey = Pidgey(deepcopy(pidgey_stats), 9, species = "pidgey")
    pidgeotto = Pidgeotto(deepcopy(pidgeotto_stats), 13, species = "pidgeotto")
    battleRNG.jump(0)

    falkner = [pidgey, pidgeotto]
    falkner_action = []
    cynda_action = []
    enemy_action = []
    cynda_hplog = []
    falkner_hp = []
    #ending hp, amount of item usage, amount of potion/s usage
    misc_info = []

    win = False

    #ending hp, amount of item usage, amount of potion/s usage
    rng_lst = []
    win = False
    for turn in range(0, len(debug_moves)):



        ai_decision = falkner[0].decide(cynda, battleRNG)
        cynda_decision = debug_moves[turn]
        rng_lst.append(battleRNG.frame)

        act, damage = cynda.useMove(cynda_decision,falkner[0],battleRNG) 
        cynda_action.append(act)

        if falkner[0].actual[0] <= 0:
            falkner_hp.append("0, dead")
            cynda_hplog.append(cynda.actual[0])
            if cynda.level == 12:
                if cynda_action[len(cynda_action)-1] == 'Ember burn':
                    cynda_action[len(cynda_action)-1] = 'Ember'
                elif cynda_action[len(cynda_action)-1] == 'Ember crit burn':
                    cynda_action[len(cynda_action)-1] = 'Ember crit'
                cynda_action[len(cynda_action)-1] += ' (killed pidgey)'
                falkner.remove(falkner[0])
                cynda.levelUp()
                battleRNG.jump(battleRNG.frame-1)
                continue
            else:
                win = True
                cynda_action[len(cynda_action)-1] += ' (win lmao)'
                break

        falkner_action.append(falkner[0].useMove(ai_decision, cynda, battleRNG))

        if cynda.actual[0] <= 0:
            win = False
            falkner_action[len(falkner_action)-1] += ' (lose)'
            cynda_hplog.append(0)
            break

        if falkner[0].burnt:
            falkner[0].actual[0] -= int(falkner[0].base_stats[0]/8)

        if falkner[0].actual[0] <= 0:
            falkner_hp.append("0, dead")
            win = True
            cynda_hplog.append(cynda.actual[0])
            if falkner[0].species == pidgey:
                cynda_action[len(cynda_action)-1] += ' (killed pidgey)'
                falkner.remove(falkner[0])
                cynda.levelUp()
                continue
            else:
                cynda_action[len(cynda_action)-1] += ' (win)'
                break
        cynda_hplog.append(cynda.actual[0])
        falkner_hp.append(falkner[0].actual[0])

    print(hex(battleRNG.seed))
    print(cynda_action)
    print(cynda_hplog)
    print(falkner_action)
    print(falkner_hp)
    print(rng_lst)
    print(win)
    battle_res.append(win)
    print()
    print()


def main():
    # cynda_lv13 = [33, 22, 18, 26, 16, 26]

    battle_seeds =  getCluster(cluster)


    battle_res = []
    battle_turns = []

    if debug_mode == True:
        debug()
        return

    for battle_seed in battle_seeds:
        battleRNG = RNG(battle_seed)

        log.start_battle(battleRNG.seed)

        #init pokemon

        cynda = Cyndaquil(deepcopy([31, 20, 17, 24, 15, 24]), 12, cynda_hp)

        print("cynda has ", cynda.actual[0], "for new battle")

        pidgey = Pidgey(deepcopy(pidgey_stats), 9, species = "pidgey")
        pidgeotto = Pidgeotto(deepcopy(pidgeotto_stats), 13, species = "pidgeotto")
        battleRNG.jump(0)

        falkner = [pidgey, pidgeotto]
        falkner_action = []
        cynda_action = []
        enemy_action = []
        cynda_hplog = []
        falkner_hp = []
        #ending hp, amount of item usage, amount of potion/s usage
        misc_info = []

        win = False

        #ending hp, amount of item usage, amount of potion/s usage
        misc_info = []
        rng_lst = []
        roark_hp = []
        win = False
        pot_count = 0

        num_turns = 0
        #Keep going so long as no one's dead
        while cynda.actual[0] > 0 and falkner[0].actual[0] > 0:

            num_turns += 1
            turn = BattleTurn()
            turn.turn_count = num_turns
            turn.cynda_hp = cynda.actual[0]

            ai_decision = falkner[0].decide(cynda, battleRNG)
            cynda_decision = cynda.decide(falkner[0], battleRNG)
            
            if cynda_decision == "pot":
                pot_count += 1

            rng_lst.append(battleRNG.frame)

            act, damage = cynda.useMove(cynda_decision,falkner[0],battleRNG) 

            print(f"Cynda did {damage} to {falkner[0].species} {falkner[0].actual[0]} HP left")
            

            turn.cynda_action = cynda_decision
            turn.opponent_action = ai_decision
            turn.cynda_roll = damage
            if act.find("crit") > -1:
                turn.cynda_crit = 1
                print(f" A critical hit !")
            elif act.find("burn") > -1:
                turn.cynda_burn = 1
                print(f"It was burned!")
            

            #Cynda killed the opponent
            if falkner[0].actual[0] <= 0:
                
                if cynda.level == 12:
                    if act == 'Ember burn':
                        act = 'Ember'
                    elif act == 'Ember crit burn':
                        act = 'Ember crit'
                    act += ' (killed pidgey)'
                    falkner_action.append("Sent out Pidgeotto")
                    falkner.remove(falkner[0])
                    cynda.levelUp()
                    battleRNG.jump(battleRNG.frame-1)
                    falkner_hp.append("0, dead")
                    cynda_hplog.append(cynda.actual[0])
                    turn.opponent_action = "Send in Pidgeotto"
                    turn.commitTurn()
                    continue

                else:
                    falkner_action.append("Dead")
                    win = True
                    cynda_action[len(cynda_action)-1] += ' (win)'
                    falkner_hp.append("0, dead")
                    cynda_hplog.append(cynda.actual[0])
                    turn.opponent_action = "Dead" 
                    turn.commitTurn()
                    break
                    

            cynda_action.append(act)

            falkner_act, damage = falkner[0].useMove(ai_decision, cynda, battleRNG)
            falkner_action.append(falkner_act)
            turn.opponent_roll = damage
            if falkner_act.find("crit") > -1:
                turn.opponent_crit = 1

            #Cynda died
            if cynda.actual[0] <= 0:
                win = False
                falkner_action[len(falkner_action)-1] += ' (lose)'
                cynda_hplog.append(0)
                turn.commitTurn()
                break

            
            if falkner[0].burnt:
                falkner[0].actual[0] -= int(falkner[0].base_stats[0]/8)
                turn.cynda_burn = 1

            if falkner[0].actual[0] <= 0:
                falkner_hp.append("0, dead")
                win = True
                cynda_hplog.append(cynda.actual[0])
                if falkner[0].species == pidgey:
                    
                    falkner_action[len(falkner_action)-1] += ' (sent out Pidgeotto)'
                    cynda_action[len(cynda_action)-1] += ' (killed pidgey)'
                    
                    #Send out Pigdeotto
                    falkner.remove(falkner[0])
                    #Level cynda
                    cynda.levelUp()

                    turn.opponent_action = "Pidgeotto"
                    turn.commitTurn()
                    continue
                else:
                    falkner_action[len(falkner_action)-1] += ' (dead to burn)'
                    cynda_action[len(cynda_action)-1] += ' (win)'
                    # turn.opponent_action = "Dead"
                    turn.commitTurn()
                    break
                    


            cynda_hplog.append(cynda.actual[0])
            falkner_hp.append(falkner[0].actual[0])

            turn.cynda_hp = cynda.actual[0]
            turn.opponent_hp = max(falkner[0].actual[0], 0)

            turn.commitTurn()

        log.mark_outcome(win)

        ifPrint = True
        

        if ifPrint:

            print(hex(battleRNG.seed))
            print(battleRNG.seed - battle_seeds[0])
            print(cynda_action)
            print(cynda_hplog)
            print(falkner_action)
            print(falkner_hp)
            print(rng_lst)
            print(win)
            battle_res.append(win)
            if win:
                battle_turns.append(len(cynda_action))
            print()
            print()

    win_num = 0
    for x in battle_res:
        if x:
            win_num += 1
    print(f"Total of {len(battle_res)}")
    if statistic:
        print(f"Total: {len(battle_res)}\nWin: {win_num}\nLose: {len(battle_res)-win_num}\nWin Rate: {win_num/len(battle_res)}\nAvg Winning Turns: {sum(battle_turns)/len(battle_turns)}")




    base = 0x0d2a
    offset = 54 * (21*60)
    end = base + offset
    print(hex(end))

    log.write_output('test.csv')
    

if __name__ == '__main__':
    main()