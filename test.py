# with_less_data.py
import io
import pprint
import sys
import math
import csv
from lib.heroes import heroes

from smoke.io.wrap import demo as io_wrp_dm
from smoke.replay import demo as rply_dm
from smoke.replay.const import Data

pp = pprint.PrettyPrinter(indent=2)
class Overview:
    """
    Parses dota2 replay file and produces over statistics
    @param string replay  the replay path
    """
    def __init__(self, replay):
        self.replay = replay
        pass
    def parse(self):
        with io.open(self.replay, 'rb') as infile:
            demo_io = io_wrp_dm.Wrap(infile)
            demo_io.bootstrap() 

            # it's a bitmask -- see smoke.replay.demo for all options
            parse = Data.All
            demo = rply_dm.Demo(demo_io, parse=parse)
            demo.bootstrap() 

            ## meta
            received_tables = demo.match.recv_tables
            class_info = demo.match.class_info
            time_offset = None
            last_minutes = -1
            prev_items = []

            game_meta_tables = received_tables.by_dt['DT_DOTAGamerulesProxy']
            game_status_index = game_meta_tables.by_name['dota_gamerules_data.m_nGameState']

            resolution = float(30)
            resolution_scale = resolution / 60
            for match in demo.play():
                items = []
                ## game data for this tick
                game_meta = match.entities.by_cls[class_info['DT_DOTAGamerulesProxy']][0].state
                current_game_status = game_meta.get(game_status_index)
                world_data = match.entities.by_cls[class_info['DT_DOTA_PlayerResource']]
                rt = received_tables.by_dt['DT_DOTA_PlayerResource']
                npc_info_table = received_tables.by_dt['DT_DOTA_BaseNPC']
                current_data = world_data[0].state

                ## index for an items name
                name_index = received_tables.by_dt['DT_DOTA_Item'].by_name['m_iName']  
                
                # Make sure the game is ongoing
                if current_game_status < 5:
                    continue
                
                ## get current game time
                time = game_meta.get(game_meta_tables.by_name['dota_gamerules_data.m_fGameTime']) - game_meta.get(game_meta_tables.by_name['dota_gamerules_data.m_flGameStartTime'])
                if time_offset is None:
                    time_offset = time
                time -= time_offset
                time_formatted = round((time / 60) * 10) / 10
                time_round = int(math.floor(time / resolution))

                if time_round > last_minutes:
                    last_minutes = time_round
                elif current_game_status < 6:
                    continue
                else:
                    winner = game_meta.get(game_meta_tables.by_name['dota_gamerules_data.m_nGameWinner'])

                # The data loop, for each player
                for i in range(10):
                    # pass
                    ## get hero meta info
                    player_id = str(i).zfill(4)
                    hero_ehandle_index = rt.by_name['m_hSelectedHero.{:04d}'.format(i)]
                    hero_id_index = rt.by_name['m_nSelectedHeroID.{:04d}'.format(i)]

                    hero_id = current_data.get(hero_id_index)
                    hero_ehandle = current_data.get(hero_ehandle_index)
                    localized_hero_name = heroes[hero_id]['localized_name']

                    hero_meta = match.entities.by_ehandle[hero_ehandle]
                    items = []
                    try:
                        ## check all inventory slots
                        for j in range(70,76): 
                            item = hero_meta.state.get(j)
                            if item not in items and item != 2097151:
                                items.append(item)
                        ## print items
                        if len(items) > 0:                    
                            for item in items:
                                item_name = match.entities.by_ehandle[item].state.get(name_index)
                                if item_name is None:
                                    continue
                                elif len(item_name) > 0 and item not in prev_items:
                                    print time_formatted, localized_hero_name, item_name
                    except KeyError, IndexError:
                        print 'error'
                    prev_items = items

test = Overview('replays/1195626066.dem')
test.parse()