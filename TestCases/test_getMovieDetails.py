import unittest
import requests
import pytest
from Utilities.ReadConfigFile import read_config
from Utilities.CustomLogger import custom_logger
import jsonpath


class Tv_programs(unittest.TestCase):
    baseurl = read_config('baseUrl', 'baseUrl')
    print(baseurl)
    key = read_config('APIKey', 'api')
    payload = "api_key="+str(read_config('APIKey', 'api'))+"&language="+str(read_config('language', 'lang'))
    log = custom_logger()

    @pytest.mark.getLatestMovies
    def test_get_latestMovies(self):
        url = str(self.baseurl)+str(read_config('type','movie'))+"/"+str(read_config('ids','latest'))
        response = requests.get(url, self.payload)
        print(response.status_code)
        print(response.json())
        # self.log.info(f"got response for the request as {response.status_code} and the response body as {response.json()} for the request getLatestMovieDetails")
        assert response.status_code == 200

    @pytest.mark.getTopRatedMovies
    def test_get_topRatedMovies(self):
        url = str(self.baseurl)+str(read_config('type','movie'))+"/"+str(read_config('ids','rated'))
        response = requests.get(url, self.payload)
        print(response.status_code)
        #self.log.info(f"got response for the request as {response.status_code} and the response body as {response.json()} for the request getTopRatedMovies")
        for i in range(len(jsonpath.jsonpath(response.json(), 'results')[0])):
            movieName = jsonpath.jsonpath(response.json(), 'results')[0][i]['title']
            vote_rating = jsonpath.jsonpath(response.json(), 'results')[0][i]['vote_average']
            print(str(movieName), "---", str(vote_rating))
            if vote_rating > float(read_config('avgRating', 'voteAvgRating')):
                print(str(vote_rating), "---", str(True))
            else:
                print(str(vote_rating), "---", str(False))

    @pytest.mark.getMovieById
    def test_get_movieById(self):
        url = str(self.baseurl)+str(read_config('type', 'movie'))+"/"+str(read_config('ids', 'movieId'))
        payload = "api_key="+str(read_config('APIKey', 'api'))
        response = requests.get(url, payload)
        print(response.status_code)
        print(response.json())
        #self.log.info(f"got response for the request as {response.status_code} and the response body as {response.json()} for the request getMovieById")
        assert response.status_code == 200
