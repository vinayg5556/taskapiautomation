import unittest
import requests
import pytest
from Utilities.ReadConfigFile import readConfig
from Utilities.CustomLogger import customLogger
import jsonpath


class tvPrograms(unittest.TestCase):
    baseUrl = readConfig('baseUrl', 'baseUrl')
    payload = f"api_key={readConfig('APIKey', 'api')}&language={readConfig('language', 'lang')}"
    log = customLogger()

    @pytest.mark.tvProgrammeDetails
    def test_getTvProgrammeDetails(self):
        url = f"{self.baseUrl}{readConfig('type', 'tv')}/{readConfig('ids', 'programmeTvId')}"
        response = requests.get(url, self.payload)
        programmeName = jsonpath.jsonpath(response.json(), 'original_name')
        print(programmeName[0])
        self.log.info(
            f"got the response status as {response.status_code} and response is {response.text} for the request getTvProgrammeDetails")
        assert response.status_code == 200
        assert programmeName[0] == "Bhagya Lakshmi"

    @pytest.mark.topRatedTvProgrammes
    def test_getTvTopRatedPrograms(self):
        url = f"{self.baseUrl}{readConfig('type', 'tv')}/{readConfig('ids', 'rated')}"
        response = requests.get(url, self.payload)
        for i in range(len(jsonpath.jsonpath(response.json(), 'results')[0])):
            ProgrammeName = jsonpath.jsonpath(response.json(), 'results')[0][i]['name']
            print(ProgrammeName)
        self.log.info(f"got the response status as {response.status_code} and response as {response.text} for the request getTopRatedTvProgrammes")
        assert response.status_code == 200

    @pytest.mark.getTvEpisodeInfo
    def test_getTvEpisodes(self):
        url = f"{self.baseUrl}{readConfig('type', 'tv')}/{readConfig('ids', 'episodesTvId')}/{readConfig('type', 'season')}/{readConfig('ids', 'seasonId')}/{readConfig('type', 'episode')}/{readConfig('ids', 'episodeId')}"
        response = requests.get(url, self.payload)
        episode = jsonpath.jsonpath(response.json(), 'episode_number')
        season = jsonpath.jsonpath(response.json(), 'season_number')
        episodeName = jsonpath.jsonpath(response.json(), 'name')
        self.log.info(f"got the response status as {response.status_code} and response as {response.text} for the request getTvEpisodesInfo")
        assert response.status_code == 200
        assert episode[0] == 1
        assert season[0] == 2
        assert episodeName[0] == "Somewhere to Start"
