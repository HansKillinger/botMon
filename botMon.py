import time
import seasonsAPI
import classicAPI
from utils import sorter, convertTime, timeLeft
from configparser import ConfigParser
from argparse import ArgumentParser

sessionID = ""
wallet = ""
config = ConfigParser()

parser = ArgumentParser()
parser.add_argument("configfile", help="config file.ini to use")

Type_Advantage = {
    1: 14,  # Insect>Leaf
    2: 16,  # Dragon>Toxin
    3: 8,  # Mystic>Telepath
    4: 9,  # Fire>Irin
    5: 2,  # Phantom>Dragon
    6: 11,  # Earth>Lightning
    7: 3,  # Neutral>Mystic
    8: 5,  # Telepath>Phantom
    9: 15,  # Iron>Ice
    11: 18,  # Lightning>Water
    12: 7,  # Combat>Neutral
    13: 6,  # Flyer>Earth
    14: 17,  # Leaf>Rock
    15: 13,  # Ice>Flyer
    16: 12,  # Toxin>Combat
    17: 1,  # Rock>Insect
    18: 4  # Water>Fire
}


def check_type_adv(mon1, mon2):
    for t in mon1['types']:
        if Type_Advantage[t] in mon2['types']:
            return True
    return False


def adjust_ancestors(ancestors: list):
    retval = ancestors
    for i in ancestors:
        if i < 221:
            retval.append(i + 1000)
    return retval


def fight(attacker: list, castle: list):
    pa_dmg = attacker[1] - castle[2]
    if pa_dmg < 10:
        pa_dmg = 10
    sa_dmg = attacker[3] - castle[4]
    if sa_dmg < 10:
        sa_dmg = 10
    if pa_dmg > sa_dmg:
        attacker.append(pa_dmg)
    else:
        attacker.append(sa_dmg)

    pa_dmg = castle[1] - attacker[2]
    if pa_dmg < 10:
        pa_dmg = 10
    sa_dmg = castle[3] - attacker[4]
    if sa_dmg < 10:
        sa_dmg = 10
    if pa_dmg > sa_dmg:
        castle.append(pa_dmg)
    else:
        castle.append(sa_dmg)
    for _i in range(0, 6):
        if attacker[5] > castle[5]:
            castle[0] -= attacker[6]
            if castle[0] < 1:
                return True
            attacker[0] -= castle[6]
            if attacker[0] < 1:
                return False
        else:
            attacker[0] -= castle[6]
            if attacker[0] < 1:
                return False
            castle[0] -= attacker[6]
            if castle[0] < 1:
                return True
    if attacker[0] > castle[0]:
        return True
    else:
        return False


class Battle:
    atk_mons = []
    def_mons = []
    is_winner = False

    def __init__(self, atk_mons, def_mons):
        self.atk_mons = atk_mons
        self.def_mons = def_mons
        win_count = 0
        for i in range(0, 3):
            self.atk_mons[i]['ancestors'] = adjust_ancestors(self.atk_mons[i]['ancestors'])
            tempa = []
            for a in self.atk_mons[i]['total_battle_stats']:
                tempa.append(a)
            self.atk_mons[i]['adj_stats'] = tempa
            self.def_mons[i]['ancestors'] = adjust_ancestors(self.def_mons[i]['ancestors'])
            tempb = []
            for b in self.def_mons[i]['total_battle_stats']:
                tempb.append(b)
            self.def_mons[i]['adj_stats'] = tempb
            if check_type_adv(self.atk_mons[i], self.def_mons[i]):
                self.atk_mons[i]['adj_stats'][1] += int(self.atk_mons[i]['total_battle_stats'][1] * .3)
                self.atk_mons[i]['adj_stats'][2] += int(self.atk_mons[i]['total_battle_stats'][2] * .3)
                self.atk_mons[i]['adj_stats'][3] += int(self.atk_mons[i]['total_battle_stats'][3] * .3)
                self.atk_mons[i]['adj_stats'][4] += int(self.atk_mons[i]['total_battle_stats'][4] * .3)
            if check_type_adv(self.def_mons[i], self.atk_mons[i]):
                self.def_mons[i]['adj_stats'][1] += int(self.def_mons[i]['total_battle_stats'][1] * .3)
                self.def_mons[i]['adj_stats'][2] += int(self.def_mons[i]['total_battle_stats'][2] * .3)
                self.def_mons[i]['adj_stats'][3] += int(self.def_mons[i]['total_battle_stats'][3] * .3)
                self.def_mons[i]['adj_stats'][4] += int(self.def_mons[i]['total_battle_stats'][4] * .3)
            for g in range(3, 6):
                # Gasons
                if self.atk_mons[g] and self.atk_mons[g]['is_gason']:
                    if self.atk_mons[g]['types'][0] in self.atk_mons[i]['types']:
                        self.atk_mons[i]['adj_stats'][2] += int(self.atk_mons[i]['total_battle_stats'][2] * .1)
                        self.atk_mons[i]['adj_stats'][4] += int(self.atk_mons[i]['total_battle_stats'][4] * .1)
                if self.def_mons[g] and self.def_mons[g]['is_gason']:
                    if self.def_mons[g]['types'][0] in self.def_mons[i]['types']:
                        self.def_mons[i]['adj_stats'][2] += int(self.def_mons[i]['total_battle_stats'][2] * .1)
                        self.def_mons[i]['adj_stats'][4] += int(self.def_mons[i]['total_battle_stats'][4] * .1)
                # Ancestors
                if self.atk_mons[g] and self.atk_mons[g]['class_id'] in self.atk_mons[i]['ancestors']:
                    self.atk_mons[i]['adj_stats'][1] += int(self.atk_mons[i]['total_battle_stats'][1] * .1)
                    self.atk_mons[i]['adj_stats'][3] += int(self.atk_mons[i]['total_battle_stats'][3] * .1)
                    # self.atk_mons[i]['adj_stats'][2] += int(self.atk_mons[i]['total_battle_stats'][2] * .1)
                    # self.atk_mons[i]['adj_stats'][4] += int(self.atk_mons[i]['total_battle_stats'][4] * .1)
                if self.def_mons[g] and self.def_mons[g]['class_id'] in self.def_mons[i]['ancestors']:
                    self.def_mons[i]['adj_stats'][1] += int(self.def_mons[i]['total_battle_stats'][1] * .1)
                    self.def_mons[i]['adj_stats'][3] += int(self.def_mons[i]['total_battle_stats'][3] * .1)
                    # self.def_mons[i]['adj_stats'][2] += int(self.def_mons[i]['total_battle_stats'][2] * .1)
                    # self.def_mons[i]['adj_stats'][4] += int(self.def_mons[i]['total_battle_stats'][4] * .1)
            if fight(self.atk_mons[i]['adj_stats'], self.def_mons[i]['adj_stats']):
                win_count += 1
            # print(f"{self.atk_mons[i]['adj_stats']} * {self.def_mons[i]['adj_stats']}")
        if win_count > 1:
            self.is_winner = True
        else:
            self.is_winner = False


def copy_value(value):
    return value


class Ladder:
    type = ''
    start_timer = 0
    end_timer = 0
    energy_end_timer = 0
    status = 'RUNNING'
    min_level = 0
    max_level = 0

    monsters = []
    current_rank = 0
    current_point = 0
    current_energy = 0
    player_id = 0

    wins = 0
    defenders = []
    is_classic = False
    is_valid = True
    only_win = True
    sort_desc = True

    def __init__(self, data):
        self.type = data['type']
        self.start_timer = data['start_timer']
        self.end_timer = data['end_timer']
        self.energy_end_timer = data['energy_end_timer']
        self.status = data['status']
        self.min_level = data['min_level']
        self.max_level = data['max_level']

        self.sort_by = 'point'

    def updateLadder(self):
        if self.is_classic:
            resp = classicAPI.get_rank_all_castles(sessionID, wallet, self.type)
        else:
            resp = seasonsAPI.get_rank_all_castles(sessionID, wallet, self.type)
        p_data = resp['data']['player_info']
        castles = resp['data']['defender_list']
        # Set player stats
        self.current_energy = p_data['current_energy']
        self.current_point = p_data['current_point']
        self.current_rank = p_data['current_rank']
        self.player_id = p_data['player_id']
        self.defenders = sorter(castles, self.sort_by, self.sort_desc)
        self.monsters = p_data['monsters']
        self.is_valid = True
        for i in range(0, 3):
            if self.monsters[i]['total_level'] > self.max_level:
                self.is_valid = False

    def fightBest(self):
        for a in range(0, len(self.defenders)):
            i = self.defenders[a]
            mons = self.monsters
            battle = Battle(mons, i['monster_info'])

            if battle.is_winner:
                if self.is_classic:
                    resp = classicAPI.attack_battle(sessionID, 1, self.player_id, i['player_id'], self.type)
                else:
                    resp = seasonsAPI.attack_battle(sessionID, 1, self.player_id, i['player_id'], self.type)
                if resp['data']['result'] == 1:
                    print('Win')
                else:
                    print('Lose')
                    for r in range(0, 3):
                        print(f"{battle.atk_mons[r]['adj_stats']} * {battle.def_mons[r]['adj_stats']}")
                time.sleep(5)
                return True

        if not self.only_win:
            i = self.defenders[0]
            mons = self.monsters
            battle = Battle(mons, i['monster_info'])
            if self.is_classic:
                resp = classicAPI.attack_battle(sessionID, 1, self.player_id, i['player_id'], self.type)
            else:
                resp = seasonsAPI.attack_battle(sessionID, 1, self.player_id, i['player_id'], self.type)
            if resp['data']['result'] == 1:
                print('Win !')
            else:
                print('Lose !')
            time.sleep(5)
            return True

        if (self.energy_end_timer - 30) > time.time() or time.time() < (self.end_timer - 30):
            time.sleep(2)
        return False


def auto_battle(is_classic=False, only_win=True):
    if is_classic:
        resp = classicAPI.get_battle_timers(sessionID=sessionID)
    else:
        resp = seasonsAPI.get_battle_timers(sessionID=sessionID)
    ladders = []
    for i in resp['data']:
        new = Ladder(resp['data'][i])
        new.is_classic = is_classic
        if new.type in config.sections():
            config_data = config[new.type]
            new.sort_by = config_data['sort_by']
            new.sort_desc = bool(int(config_data['sort_desc']))
            new.only_win = bool(int(config_data['only_win']))
            ladders.append(new)
    ladders_list = []
    for i in ladders:
        ladders_list.append(i.type)
    while len(ladders_list) > 0:
        for i in ladders:
            if i.energy_end_timer < time.time() or time.time() > i.end_timer:
                ladders_list.remove(i.type)
            if i.type in ladders_list:
                i.updateLadder()
                print(f"({convertTime(timeLeft(i.energy_end_timer))}){i.type} * Energy: {i.current_energy}", end=' ')
                if not i.is_valid:
                    print('Invalid Team Removed')
                    ladders_list.remove(i.type)
                else:
                    if i.current_energy > 0:
                        if not i.fightBest():
                            print('Pass')
                    else:
                        ladders_list.remove(i.type)
                        print('Removed')


if __name__ == '__main__':
    args = parser.parse_args()
    config.read(args.configfile)
    bot_settings = config['settings']
    wallet = bot_settings['wallet']
    sessionID = bot_settings['sessionid']
    auto_battle(bool(int(bot_settings['is_classic'])))
