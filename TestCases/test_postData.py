import unittest

import jsonpath
import pytest
import requests
import json
from Utilities.CustomLogger import customLogger
from Utilities.ReadConfigFile import readConfig
from TestCases.test_getRequestToken import test_createSession


class postData(unittest.TestCase):
    log = customLogger()

    @pytest.mark.postMovieRating
    def test_postMovieRating(self):
        sessionId = test_createSession()
        file = open("..//Data/postRating.json", 'r')
        jsonData = json.loads(file.read())
        url = f"{readConfig('baseUrl', 'baseUrl')}{readConfig('type', 'movie')}/{readConfig('ids', 'movieId')}/rating?api_key={readConfig('APIKey', 'api')}&session_id={sessionId}"
        response = requests.post(url, jsonData)
        print(response.status_code)
        print(response.text)
        statusMessage = jsonpath.jsonpath(response.json(), "status_message")[0]
        self.log.info(
            f"got response from server as {response.status_code} and the response body as {response.json()} for the request postMovieRating")
        assert response.status_code == 201
        assert statusMessage == "The item/record was updated successfully."
        
