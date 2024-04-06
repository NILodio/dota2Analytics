import logging
import os
import time  # Import time module for rate limiting

import pandas as pd
import requests


class OpenDotaAPI(object):
    def __init__(self, output_filepath=None):
        self.api_key = os.getenv("OPEN_DOTA_KEY")
        self.base_url = "https://api.opendota.com/api/"
        self.rate_limit = 1.0
        self.start_match_id = os.getenv("START_MATCH_ID")
        self.logger = logging.getLogger(__name__)
        self.output_filepath = "data/raw" if not output_filepath else output_filepath

    def get_pro_matches(self, num_matches=20000, batch_size=100):
        """
        Get a list of matches.

        Args:
            num_matches (int): Number of matches to fetch.
            batch_size (int): Number of matches to fetch in each API call.

        Returns:
            pandas.DataFrame: DataFrame containing match details.
        """
        pro_matches = []
        match_info = []
        remaining_matches = num_matches
        while remaining_matches > 0:
            current_batch_size = min(remaining_matches, batch_size)
            endpoint = f"proMatches?less_than_match_id={self.start_match_id}"
            response = self._make_request(endpoint)
            match_tem = []
            for match in response:
                r_match = self.get_matche_info(match["match_id"])
                match_tem.append(r_match)
                time.sleep(self.rate_limit)
            self.logger.info(f"Fetched {len(response)} matches")
            pro_matches.extend(response)
            match_info.extend(match_tem)
            if len(response) < current_batch_size:
                break
            self.start_match_id = response[-1]["match_id"] - 1
            remaining_matches -= current_batch_size
            time.sleep(self.rate_limit)

        return pd.DataFrame(pro_matches), pd.DataFrame(match_info)

    def get_matche_info(self, match_id):
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

        if not response:
            return {
                "match_id": match_id,
                "barracks_status_dire": None,
                "barracks_status_radiant": None,
                "cluster": None,
                "dire_score": None,
                "engine": None,
                "first_blood_time": None,
                "game_mode": None,
                "radiant_win": None,
                "human_players": None,
                "leagueid": None,
                "lobby_type": None,
                "match_seq_num": None,
                "radiant_score": None,
                "duration": None,
                "tower_status_dire": None,
                "tower_status_radiant": None,
                "skill": None,
                "region": None,
                "throw": None,
                "comeback": None,
                "loss": None,
                "win": None,
                "start_time": None,
            }
        else:
            return {
                "match_id": response["match_id"],
                "barracks_status_dire": response["barracks_status_dire"],
                "barracks_status_radiant": response["barracks_status_radiant"],
                "cluster": response["cluster"],
                "dire_score": response["dire_score"],
                "engine": response["engine"],
                "first_blood_time": response["first_blood_time"],
                "game_mode": response["game_mode"],
                "radiant_win": response["radiant_win"],
                "human_players": response["human_players"],
                "leagueid": response["leagueid"],
                "lobby_type": response["lobby_type"],
                "match_seq_num": response["match_seq_num"],
                "radiant_score": response["radiant_score"],
                "duration": response["duration"],
                "tower_status_dire": response["tower_status_dire"],
                "tower_status_radiant": response["tower_status_radiant"],
                "skill": response["skill"] if "skils" in response else None,
                "region": response["region"] if "region" in response else None,
                "throw": response["throw"] if "throw" in response else None,
                "comeback": response["comeback"] if "comeback" in response else None,
                "loss": response["loss"] if "loss" in response else None,
                "win": response["win"] if "win" in response else None,
                "start_time": response["start_time"],
            }

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
            return response.json()
        else:
            return {}
