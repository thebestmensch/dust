import sys
import os
import math
import csv
import io
import pandas as pd
import numpy as np

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

            ## smoke parses the demo file
            parse = Data.All ^ (Data.GameEvents | Data.TempEntities)
            demo = rply_dm.Demo(demo_io, parse=parse)
            demo.bootstrap() 

            ## meta
            received_tables = demo.match.recv_tables
            class_info = demo.match.class_info

            ## get the internal match id
            match_id = self.getMatchID(replay)

            ## the output list
            ## match_id | hero | item_x_name | item_x_time
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
                game_time = self.getTimer(game_meta.get(game_meta_tables.by_name['dota_gamerules_data.m_fGameTime']), game_meta.get(game_meta_tables.by_name['dota_gamerules_data.m_flGameStartTime']))

                # # The data loop, for each player
                for i in range(10):
                    # pass
                    ## get hero meta info
                    player_id = str(i).zfill(4)
                    hero_ehandle_index = rt.by_name['m_hSelectedHero.{:04d}'.format(i)]
                    hero_id_index = rt.by_name['m_nSelectedHeroID.{:04d}'.format(i)]

                    hero_id = current_data.get(hero_id_index)
                    hero_ehandle = current_data.get(hero_ehandle_index)
                    localized_hero_name = heroes[hero_id]['name']

                    hero_meta = match.entities.by_ehandle[hero_ehandle]

                    try:
                        ## check all inventory slots
                        for j in range(70,76): 
                            item = hero_meta.state.get(j)
                            ## if item is not null
                            if item != 2097151:
                                item_name = match.entities.by_ehandle[item].state.get(name_index)
                                if item_name is not None and len(item_name) > 0:
                                    output.append([match_id, localized_hero_name, item_name, game_time])
                    except KeyError, IndexError:
                        pass
            ## dataframe preparation
            res = pd.DataFrame(output, columns=['match_id', 'hero_name', 'item', 'item_purchase_time'])
            res = res.drop_duplicates(['match_id','hero_name', 'item'], take_last=False)
            res = res.sort(['hero_name','item_purchase_time'], ascending=True)
            res = res.reset_index(drop=True)
            res.index.name = 'id'
            return res
    def getTimer(self, game_time, start_time):
        """
        Returns formatted game time
        @param int game_time   the current total time in game (including pick/ban stage, etc)
        @param int start_time  the total time where the game timer started (0:00 on the clock)
        @return int the game time in seconds
        """
        raw_time = game_time - start_time
        return round((raw_time / 60) * 100) / 100
    def getMatchID(self, replay):
        with io.open(replay, 'rb') as infile:
            demo_io = io_wrp_dm.Wrap(infile)
            
            ## returns offset to overview
            overview_offset = demo_io.bootstrap() 
            
            ## we can seek on the raw underlying IO instead of parsing everything
            infile.seek(overview_offset)

            demo = rply_dm.Demo(demo_io)
            demo.finish()

            ## get the raw overview data
            data = demo.match.overview
            return data['game']['match_id']





