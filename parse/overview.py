import io
import pandas as pd
import numpy as np

from lib.heroes import heroes
from smoke.io.wrap import demo as io_wrp_dm
from smoke.replay import demo as rply_dm
from smoke.replay.demo import Data

class Overview(object):
	"""
	Parses replay for match overview data

	@author		james@jamesmensch.com
	@version 	0.0.1
	@since 		2015-02-12
	"""
	def parse(self, replay):
		"""
		Parses the replay
		@param string replay  the path to the replay .dem
		@return dataframe output  the resulting overview data
		"""
		## output dataframe
		# match_id | match_length | steam_id | player_name | hero | team | outcome | banned_heroes (optional)
		output = []
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
			match_id = data['game']['match_id']
			match_length = round((data['playback']['time'] / 60) * 100) / 100
			match_winner = 'radiant' if data['game']['game_winner'] == 2 else 'dire'
			## find 
			dire_bans = []
			radiant_bans = []
			add_ban_flag = False
			for hero in data['game']['hero_selections']:
				if hero['is_pick'] is False:
					localized_name = heroes[int(hero['hero_id'])]['localized_name']
					if hero['team'] == 2:
						radiant_bans.append(str(localized_name))
					else:
						dire_bans.append(str(localized_name))
			## if the bans are the same length, we can add them to the output
			## else add nulls
			if len(dire_bans) == len(radiant_bans) and len(dire_bans) > 0:
				add_ban_flag = True
			elif len(dire_bans) > len(radiant_bans):
				num = len(dire_bans) - len(radiant_bans)
				for i in range(num):
					radiant_bans.append('null')
				add_ban_flag = True
			elif len(dire_bans) < len(radiant_bans):
				num = len(radiant_bans) - len(dire_bans)
				for i in range(num):
					dire_bans.append('null')
				add_ban_flag = True
			elif len(dire_bans) == 0:
				dire_bans += ['null', 'null', 'null', 'null', 'null']
				radiant_bans += ['null', 'null', 'null', 'null', 'null']
				add_ban_flag = True
			else:
				print dire_bans, radiant_bans

			## for each player
			for i in range(10):
				curr_player = data['game']['players'][i]
				# localized_hero_name = heroes[str(curr_player['hero_name'])]['localized_name']
				localized_hero_name = str(curr_player['hero_name'])
				game_team = 'radiant' if curr_player['game_team'] == 2 else 'dire'
				out = [int(match_id), match_length, int(curr_player['steam_id']), localized_hero_name, game_team, match_winner]
				if add_ban_flag:
					out += radiant_bans if curr_player['game_team'] == 2 else dire_bans
				output.append(out)
		## output dataframe
		columns = ['match_id', 'match_length', 'player_steam_id', 'hero_name', 'player_game_team', 'game_outcome', 'ban_1', 'ban_2', 'ban_3', 'ban_4', 'ban_5']
		try:
			res = pd.DataFrame(output, columns=columns)
			res.index.name = 'id'
			return res
		except AssertionError:
			print output[len(output)-1]
