import unittest
import requests
import pytest
from Utilities.ReadConfigFile import read_config
from Utilities.CustomLogger import custom_logger
import jsonpath


class Tv_programs(unittest.TestCase):
    baseUrl = read_config('baseUrl', 'baseUrl')
    payload = f"api_key={read_config('APIKey', 'api')}&language={read_config('language', 'lang')}"
    log = custom_logger()

    @pytest.mark.tvProgrammeDetails
    def test_get_tv_programme_details(self):
        url = f"{self.baseUrl}{read_config('type', 'tv')}/{read_config('ids', 'programmeTvId')}"
        response = requests.get(url, self.payload)
        programmeName = jsonpath.jsonpath(response.json(), 'original_name')
        print(programmeName[0])
        self.log.info(
            f"got the response status as {response.status_code} and response is {response.text} for the request getTvProgrammeDetails")
        assert response.status_code == 200
        assert programmeName[0] == "Bhagya Lakshmi"

    @pytest.mark.topRatedTvProgrammes
    def test_get_tv_top_rated_programs(self):
        url = f"{self.baseUrl}{read_config('type', 'tv')}/{read_config('ids', 'rated')}"
        response = requests.get(url, self.payload)
        for i in range(len(jsonpath.jsonpath(response.json(), 'results')[0])):
            ProgrammeName = jsonpath.jsonpath(response.json(), 'results')[0][i]['name']
            print(ProgrammeName)
        self.log.info(f"got the response status as {response.status_code} and response as {response.text} for the request getTopRatedTvProgrammes")
        assert response.status_code == 200

    @pytest.mark.getTvEpisodeInfo
    def test_get_tv_episodes(self):
        url = f"{self.baseUrl}{read_config('type', 'tv')}/{read_config('ids', 'episodesTvId')}/{read_config('type', 'season')}/{read_config('ids', 'seasonId')}/{read_config('type', 'episode')}/{read_config('ids', 'episodeId')}"
        response = requests.get(url, self.payload)
        episode = jsonpath.jsonpath(response.json(), 'episode_number')
        season = jsonpath.jsonpath(response.json(), 'season_number')
        episodeName = jsonpath.jsonpath(response.json(), 'name')
        self.log.info(f"got the response status as {response.status_code} and response as {response.text} for the request getTvEpisodesInfo")
        assert response.status_code == 200
        assert episode[0] == 1
        assert season[0] == 2
        assert episodeName[0] == "Somewhere to Start"
