import logging
import os
import time  # Import time module for rate limiting

import pandas as pd
import requests


class OpenDotaAPI(object):
    def __init__(self, output_filepath=None):
        self.api_key = os.getenv("OPEN_DOTA_KEY")
        self.base_url = "https://api.opendota.com/api/"
        self.rate_limit = 0.2
        self.start_match_id = os.getenv("START_MATCH_ID")
        self.logger = logging.getLogger(__name__)
        self.output_filepath = "data/raw" if not output_filepath else output_filepath

    def get_pro_matches(self, num_matches=100, batch_size=100):
        """
        Get a dataframe of the pro match data.

        Args:
            num_matches (int): Number of matches to fetch.
            batch_size (int): Number of matches to fetch in each API call.

        Returns:
            pandas.DataFrame: DataFrame containing match details.
        """
        matches = []
        remaining_matches = num_matches
        while remaining_matches > 0:
            current_batch_size = min(remaining_matches, batch_size)
            response = self.get_pro_match_info(self.start_match_id)
            print("Remaining matches:", remaining_matches, "- Response length:", len(response))

            for match in response:
                print("Match #", len(matches), "- Match ID:", match["match_id"])
                r_match = self.get_match_info(match["match_id"])
                r_team_1_info = self.get_team_info(match["radiant_team_id"])
                r_team_2_info = self.get_team_info(match["dire_team_id"])
                r_team_1_players = self.get_team_players_info(match["radiant_team_id"])
                r_team_2_players = self.get_team_players_info(match["dire_team_id"])
                r_team_1_heroes = self.get_team_heroes_info(match["radiant_team_id"])
                r_team_2_heroes = self.get_team_heroes_info(match["dire_team_id"])

                match_dict = self.set_match_data(match, r_match, r_team_1_info, r_team_2_info, r_team_1_players, r_team_2_players, r_team_1_heroes, r_team_2_heroes)
                matches.append(match_dict)

                time.sleep(self.rate_limit)

            self.logger.info(f"Fetched {len(response)} matches")
            if len(response) < current_batch_size:
                break
            self.start_match_id = response[-1]["match_id"] - 1
            remaining_matches -= current_batch_size
            time.sleep(self.rate_limit)

        return pd.DataFrame(matches)

    def set_match_data(self, promatch_data, match_data, team1_data, team2_data, team1players_data, team2players_data, team1heroes_data, team2heroes_data):
        """
        Build the dictionary that will result in the final row of the dataframe
        For that we need to use all the data we have collected for the match

        Args:
            promatch_data (dictionary): data from get_pro_match_info
            match_data (dictionary): data from get_match_info
            team1_data (dictionary): data from get_team_info (for team 1)
            team2_data (dictionary): data from get_team_info (for team 2)
            team1players_data (list): data from get_team_players_info (for team 1)
            team2players_data (list): data from get_team_players_info (for team 2)

        Returns:
            dictionary containing the final row of the dataset with all data combined
        """
        # add match columns
        match = promatch_data.copy()
        match["region"] = match_data["region"]

        # add picks and bans columns
        match = self.add_picks_bans_data(match, match_data["picks_bans"])

        # add team 1 columns
        match["team1_id"] = team1_data["team_id"]
        match["team1_rating"] = team1_data["rating"]
        match["team1_wins"] = team1_data["wins"]
        match["team1_losses"] = team1_data["losses"]
        match["team1_last_match_time"] = team1_data["last_match_time"]

        # add team 2 columns
        match["team2_id"] = team2_data["team_id"]
        match["team2_rating"] = team2_data["rating"]
        match["team2_wins"] = team2_data["wins"]
        match["team2_losses"] = team2_data["losses"]
        match["team2_last_match_time"] = team2_data["last_match_time"]

        # add team 1 players columns
        match = self.add_players_data(match, match_data["players"], team1players_data, "1")
        # add team 2 players columns
        match = self.add_players_data(match, match_data["players"], team2players_data, "2")

        # add team 1 heroes columns
        match = self.add_heroes_data(match, team1heroes_data, "1")
        # add team 2 heroes columns
        match = self.add_heroes_data(match, team2heroes_data, "2")

        return match

    def add_heroes_data(self, match, team_heroes_, team_number):
        team_heroes = {}
        if team_heroes_ is not None:
            for hero in team_heroes_:
                team_heroes[hero['hero_id']] = {"games_played" : hero['games_played'], "wins" : hero['wins']}

        for i in range(1, 6):
            column_name = "team" + team_number + "_hero" + str(i)
            hero_id = match[column_name]
            match[column_name + "_gamesPlayed"] = team_heroes[hero_id]["games_played"] if hero_id in team_heroes else None
            match[column_name + "_wins"] = team_heroes[hero_id]["wins"] if hero_id in team_heroes else None

        return match

    def add_players_data(self, match, match_players, team_players_, team_number):

        # dictionary of all players that are OR WERE in the team
        team_players = {}
        if team_players_ is not None:
            for player in team_players_:
                team_players[player['account_id']] = {'games_played': player['games_played'], 'wins': player['wins']}

        count_team_players = 0
        if match_players is None:
            for i in range(1, 6):
                column_name = "team" + team_number + "_player" + str(i)
                match[column_name + "_id"] = None
                match[column_name + "_gamesPlayed"] = None
                match[column_name + "_wins"] = None
            return match

        for player in match_players:

            if team_number == "1" and player['player_slot'] >= 128:
                continue
            if team_number == "2" and player['player_slot'] < 128:
                continue

            count_team_players += 1
            column_name = "team" + team_number + "_player" + str(count_team_players)
            match[column_name + "_id"] = player['account_id']
            if player['account_id'] in team_players:
                match[column_name + "_gamesPlayed"] = team_players[player['account_id']]['games_played']
                match[column_name + "_wins"] = team_players[player['account_id']]['wins']
            else:
                match[column_name + "_gamesPlayed"] = None
                match[column_name + "_wins"] = None

        return match


    def add_picks_bans_data(self, match, picks_bans):

        if picks_bans is None:
            for i in range(1, 6):
                match["team1_hero" + str(i)] = None
            for i in range(1, 6):
                match["team2_hero" + str(i)] = None
            for i in range(1, 8):
                match["team1_ban" + str(i)] = None
            for i in range(1, 8):
                match["team2_ban" + str(i)] = None
            return match

        count_picks_team1 = 0
        count_picks_team2 = 0
        count_bans_team1 = 0
        count_bans_team2 = 0
        for pb in picks_bans: # pb is a dictionary with following fields: {'is_pick': False, 'hero_id': 66, 'team': 0/1, 'order': 0}

            if pb['is_pick'] and pb['team'] == 0: # pick from team 1
                count_picks_team1 += 1
                column_name = "team1_hero" + str(count_picks_team1)
                match[column_name] = pb['hero_id']
                continue

            elif pb['is_pick'] and pb['team'] == 1: # pick from team 2
                count_picks_team2 += 1
                column_name = "team2_hero" + str(count_picks_team2)
                match[column_name] = pb['hero_id']
                continue

            elif not pb['is_pick'] and pb['team'] == 0: # ban from team 1
                count_bans_team1 += 1
                column_name = "team1_ban" + str(count_bans_team1)
                match[column_name] = pb['hero_id']
                continue

            elif not pb['is_pick'] and pb['team'] == 1: # ban from team 2
                count_bans_team2 += 1
                column_name = "team2_ban" + str(count_bans_team2)
                match[column_name] = pb['hero_id']
                continue

        return match

    def get_pro_match_info(self, match_id):

        endpoint = f"proMatches?less_than_match_id={match_id}"

        response = self._make_request(endpoint)

        if not response:
            return []

        pro_matches = []
        for match in response:
            pro_match_dict = {
                "match_id" : match["match_id"] if "match_id" in match else None,
                "start_time" : match["start_time"] if "start_time" in match else None,
                "radiant_team_id": match["radiant_team_id"] if "radiant_team_id" in match else None,
                "radiant_name": match["radiant_name"] if "radiant_name" in match else None,
                "dire_team_id": match["dire_team_id"] if "dire_team_id" in match else None,
                "dire_name" : match["dire_name"] if "dire_name" in match else None,
                "leagueid" : match["leagueid"] if "leagueid" in match else None,
                "league_name": match["league_name"] if "league_name" in match else None,
                "series_type": match["series_type"] if "series_type" in match else None,
                "radiant_win": match["radiant_win"] if "radiant_win" in match else None
            }
            pro_matches.append(pro_match_dict)
        return pro_matches

    def get_match_info(self, match_id):
        """
        Get a list of matches with info.

        Args:
            data (list): List of match ids.
            batch_size (int): Number of matches to fetch in each API call.

        Returns:
            pandas.DataFrame: DataFrame containing match details.
        """
        endpoint = f"matches/{match_id}"

        response = self._make_request(endpoint)

        players = []
        if "players" in response:
            for player in response["players"]:
                players.append({"account_id": player["account_id"], "player_slot": player["player_slot"]})

        if not response:
            return {
                "match_id": match_id,
                "picks_bans": None,
                "region": None,
                "players": None
            }
        else:
            return {
                "match_id": response["match_id"],
                "picks_bans": response["picks_bans"] if 'picks_bans' in response else None,
                "region": response["region"] if "region" in response else None,
                "players": players
            }

    def get_team_info(self, team_id):
        """
        Get the team data

        Args:
            team_id (int): id of the team

        Returns:
            Python dictionary containing team team data
        """
        endpoint = f"teams/{team_id}"

        response = self._make_request(endpoint)

        if not response:
            return {
                "team_id": team_id,
                "rating": None,
                "wins": None,
                "losses": None,
                "last_match_time": None
            }
        else:
            return {
                "team_id": response["team_id"],
                "rating": response["rating"] if 'rating' in response else None,
                "wins": response["wins"] if "wins" in response else None,
                "losses": response["losses"] if 'losses' in response else None,
                "last_match_time": response["last_match_time"] if "last_match_time" in response else None
            }

    def get_team_heroes_info(self, team_id):

        endpoint = f"teams/{team_id}/heroes"

        response = self._make_request(endpoint)

        if not response:
            return []
        else:
            return response

    def get_team_players_info(self, team_id):
        """
        Get the team players data

        Args:
            team_id (int): id of the team

        Returns:
            Python list containing team players
        """
        endpoint = f"teams/{team_id}/players"

        response = self._make_request(endpoint)

        if not response:
            return []
        else:
            return response


    def _make_request(self, endpoint):
        """
        Make a request to the OpenDota API.

        Args:
            endpoint (str): The API endpoint.

        Returns:
            list: Response from the API.
        """
        url = f"{self.base_url}{endpoint}"
        headers = {"Content-Type": "application/json"}
        params = {"api_key": self.api_key}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            try:
                return response.json()
            except:
                # if len(str(response)) == 16:
                return {}
        else:
            return {}
