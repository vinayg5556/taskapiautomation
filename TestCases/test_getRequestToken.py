import time

import pytest
import requests
import jsonpath
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from Utilities.ReadConfigFile import readConfig
from Utilities.CustomLogger import customLogger


apiToken = readConfig('APIKey', 'api')
log = customLogger()

@pytest.mark.tokenGenerate
def test_generateToken():
    url = f"{readConfig('baseUrl', 'baseUrl')}authentication/token/new"
    payload = f"api_key={apiToken}"
    response = requests.get(url, payload)
    print("token response", str(response.json()))
    token = jsonpath.jsonpath(response.json(), 'request_token')[0]
    log.info(f"token has been generated for the request and token is {token} and the response from serever is {response.status_code} for generateToken request")
    assert response.status_code == 200
    return token


requestToken = test_generateToken()


@pytest.mark.approveRequest
def test_getApproveRequest():
    print(requestToken)
    time.sleep(5)
    url = f"http://www.themoviedb.org/authenticate/{requestToken}"
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.maximize_window()
    driver.implicitly_wait(15)
    driver.get(url)
    driver.find_element(By.XPATH, "//*[@id='onetrust-accept-btn-handler']").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//*[@id='main']/section/div/div/div[1]/a").click()
    driver.find_element(By.XPATH, "//*[@id='username']").send_keys("testuser5556")
    driver.find_element(By.XPATH, "//*[@id='password']").send_keys("Achala@123")
    time.sleep(2)
    driver.find_element(By.XPATH, "//*[@id='login_button']").click()
    time.sleep(5)
    driver.find_element(By.XPATH, "//button[@id='allow_authentication']").click()
    time.sleep(3)
    driver.quit()
    log.info("approve request has been completed")


@pytest.mark.createSession
def test_createSession():
    test_getApproveRequest()
    url = f"https://api.themoviedb.org/3/authentication/session/new?api_key={apiToken}&request_token={requestToken}"
    response = requests.post(url)
    print(response.status_code)
    print(response.json())
    sessionId = jsonpath.jsonpath(response.json(), "session_id")[0]
    success = jsonpath.jsonpath(response.json(), "success")[0]
    print(sessionId)
    log.info(f"got response from server as {response.status_code} and the response body is {response.json()} for the request createSession")
    assert response.status_code == 200
    assert str(success) == "True"
    return sessionId
