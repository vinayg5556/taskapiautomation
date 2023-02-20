import unittest
import requests
import pytest
from Utilities.ReadConfigFile import readConfig
from Utilities.CustomLogger import customLogger
import jsonpath


class Tv_programs(unittest.TestCase):
    baseurl = readConfig('baseUrl', 'baseUrl')
    print(baseurl)
    payload = f"api_key={readConfig('APIKey', 'api')}&language={readConfig('language', 'lang')}"
    log = customLogger()

    @pytest.mark.getLatestMovies
    def test_get_latestMovies(self):
        url = f"{self.baseurl}{readConfig('type','movie')}/{readConfig('ids','latest')}"
        response = requests.get(url, self.payload)
        print(response.status_code)
        print(response.json())
        self.log.info(f"got response for the request as {response.status_code} and the response body as {response.json()} for the request getLatestMovieDetails")
        assert response.status_code == 200

    @pytest.mark.getTopRatedMovies
    def test_get_topRatedMovies(self):
        url = f"{self.baseurl}{readConfig('type','movie')}/{readConfig('ids','rated')}"
        response = requests.get(url, self.payload)
        print(response.status_code)
        self.log.info(
            f"got response for the request as {response.status_code} and the response body as {response.json()} for the request getTopRatedMovies")
        for i in range(len(jsonpath.jsonpath(response.json(), 'results')[0])):
            movieName = jsonpath.jsonpath(response.json(), 'results')[0][i]['title']
            vote_rating = jsonpath.jsonpath(response.json(), 'results')[0][i]['vote_average']
            print(str(movieName), "---", str(vote_rating))
            if vote_rating > float(readConfig('avgRating', 'voteAvgRating')):
                print(str(vote_rating), "---", str(True))
            else:
                print(str(vote_rating), "---", str(False))

    @pytest.mark.getMovieById
    def test_get_movieById(self):
        url = f"{self.baseurl}{readConfig('type', 'movie')}/{readConfig('ids', 'movieId')}"
        payload = f"api_key={readConfig('APIKey', 'api')}"
        response = requests.get(url, payload)
        print(response.status_code)
        print(response.json())
        self.log.info(
            f"got response for the request as {response.status_code} and the response body as {response.json()} for the request getMovieById")
        assert response.status_code == 200
