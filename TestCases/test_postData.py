import unittest

import jsonpath
import pytest
import requests
import json
from Utilities.CustomLogger import custom_logger
from Utilities.ReadConfigFile import read_config
from TestCases.test_getRequestToken import test_create_session


class Post_data(unittest.TestCase):
    log = custom_logger()

    @pytest.mark.postMovieRating
    def test_post_movie_rating(self):
        sessionId = test_create_session()
        file = open("..//Data/postRating.json", 'r')
        jsonData = json.loads(file.read())
        url = f"{read_config('baseUrl', 'baseUrl')}{read_config('type', 'movie')}/{read_config('ids', 'movieId')}/rating?api_key={read_config('APIKey', 'api')}&session_id={sessionId}"
        response = requests.post(url, jsonData)
        print(response.status_code)
        print(response.text)
        statusMessage = jsonpath.jsonpath(response.json(), "status_message")[0]
        self.log.info(
            f"got response from server as {response.status_code} and the response body as {response.json()} for the request postMovieRating")
        assert response.status_code == 201
        assert statusMessage == "The item/record was updated successfully."
        
