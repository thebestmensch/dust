import sys
import os
import math
import csv
import io

from lib.heroes import heroes
from smoke.io.wrap import demo as io_wrp_dm
from smoke.replay import demo as rply_dm
from smoke.replay.const import Data
from smoke.replay.demo import Data
"""
Parses replay for each heroe's item purchase times

@author     james@temboinc.com
@version    0.0.1
@since      2015-02-12
"""
class ItemTimings(object):
    """
    Parses dota2 replay file for item purchase times
    @param string replay  the replay path
    """
    def parse(self, replay):
        with io.open(replay, 'rb') as infile:
            demo_io = io_wrp_dm.Wrap(infile)
            demo_io.bootstrap() 

            parse = Data.All ^ (Data.GameEvents | Data.TempEntities)
            demo = rply_dm.Demo(demo_io, parse=parse)
            demo.bootstrap() 

            ## meta
            received_tables = demo.match.recv_tables
            class_info = demo.match.class_info
            time_offset = None

            ## the output list
            output = []

            ## find where the game_status data is located
            game_meta_tables = received_tables.by_dt['DT_DOTAGamerulesProxy']
            game_status_index = game_meta_tables.by_name['dota_gamerules_data.m_nGameState']

            for match in demo.play():
                ## game data for this tick
                game_meta = match.entities.by_cls[class_info['DT_DOTAGamerulesProxy']][0].state
                current_game_status = game_meta.get(game_status_index)
                world_data = match.entities.by_cls[class_info['DT_DOTA_PlayerResource']]
                rt = received_tables.by_dt['DT_DOTA_PlayerResource']
                current_data = world_data[0].state

                ## index for an item's name
                name_index = received_tables.by_dt['DT_DOTA_Item'].by_name['m_iName']  
                
                ## Make sure the game is ongoing
                if current_game_status < 5:
                    continue
                
                ## get current game time
                time = game_meta.get(game_meta_tables.by_name['dota_gamerules_data.m_fGameTime']) - game_meta.get(game_meta_tables.by_name['dota_gamerules_data.m_flGameStartTime'])
                if time_offset is None:
                    time_offset = time

                time -= time_offset
                time_formatted = round((time / 60) * 10) / 10
                resolution = float(30)
                resolution_scale = resolution / 60
                time_round = int(math.floor(time / resolution))

                ## 
                # if current_game_status < 6:
                #     continue
                # else:
                #     match_id = game_meta.get(game_meta_tables.by_name['dota_gamerules_data.m_nMatchID'])
                #     winner = game_meta.get(game_meta_tables.by_name['dota_gamerules_data.m_nGameWinner'])
                if current_game_status == 6:
                    # print game_meta.get(game_meta_tables.by_name['dota_gamerules_data.m_unMatchID'])
                    
                # # The data loop, for each player
                # for i in range(10):
                #     # pass
                #     ## get hero meta info
                #     player_id = str(i).zfill(4)
                #     hero_ehandle_index = rt.by_name['m_hSelectedHero.{:04d}'.format(i)]
                #     hero_id_index = rt.by_name['m_nSelectedHeroID.{:04d}'.format(i)]

                #     hero_id = current_data.get(hero_id_index)
                #     hero_ehandle = current_data.get(hero_ehandle_index)
                #     localized_hero_name = heroes[hero_id]['localized_name']

                #     hero_meta = match.entities.by_ehandle[hero_ehandle]

                #     try:
                #         ## check all inventory slots
                #         for j in range(70,76): 
                #             item = hero_meta.state.get(j)
                #             ## if item is not null
                #             if item != 2097151:
                #                 item_name = match.entities.by_ehandle[item].state.get(name_index)
                #                 if len(item_name) == 0:
                #                     continue
                #                 if localized_hero_name not in items:
                #                     items[str(localized_hero_name)] = []
                #                 ## add item to hero list if it doesn't exist already
                #                 if len([tup for tup in items[localized_hero_name] if tup[1] == item_name]) == 0:
                #                     items[localized_hero_name].append((time_formatted, item_name))
                #     except KeyError, IndexError:
                #         pass
            return output