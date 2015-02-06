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
            game_meta_tables = received_tables.by_dt['DT_DOTAGamerulesProxy']
            game_status_index = game_meta_tables.by_name['dota_gamerules_data.m_nGameState']

            # resolution = float(30)
            # resolution_scale = resolution / 60
            try:    
                for match in demo.play():
                    game_meta = match.entities.by_cls[class_info['DT_DOTAGamerulesProxy']][0].state
                    current_game_status = game_meta.get(game_status_index)
                    print game_meta.get(game_meta_tables.by_name['dota_gamerules_data.m_flGameEndTime'])
                    # Make sure the game is ongoing
                    if current_game_status < 5:
                        continue
                    if current_game_status == 6:
                        continue;
                    time = game_meta.get(game_meta_tables.by_name['dota_gamerules_data.m_fGameTime']) - game_meta.get(game_meta_tables.by_name['dota_gamerules_data.m_flGameStartTime'])
                    # print time / 60
            except IndexError:
                print 'indexerror'
        # parses game overview found at the end of the demo file
        # demo.finish()

test = Overview('replays/1215173364.dem')
test.parse()