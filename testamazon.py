import os
import time
from datetime import datetime
from appium import webdriver
from conftest import MakeDriver
#from pages.android.splash_page import DiscoveryAndroidSplashPage
# from pages.ios.splash_page import WayfairIOSSplashPage


from apis.hs_apis import HS_API

from apis.hs_logger import logger, setup_logger

class TestAmazon(object):

    api_token = os.getenv("HS_API_TOKEN")
    api = HS_API(api_token)
    now = datetime.now()
    date_time = now.strftime("%b-%d-%Y, %H:%M:%S")

    # def test_android(self: 'TestAmazon', make_driver: MakeDriver) -> None:
    #     d: webdriver.Remote = make_driver("discovery_android")
    #     time.sleep(5)
    #     splash_page = DiscoveryAndroidSplashPage(d)
    #     ts = splash_page.validate_homepage()
    #     time.sleep(5)
    #     self.api.page_load(d.session_id, ts[0], ts[1])
    #     self.api.name_session(d.session_id, "Cold Start Android {}".format(self.date_time), "Test script using appiums python library to mesaure cold start of the Discovery Plus Application")


    def getTime(time):
        # hours = 0
        # minutes = 0
        # seconds = 0
        if time.count(':') == 1:
            spot = time.find(':')
            minutes = time[0:spot]
            seconds = time[spot+1:len(time)]
            return int(minutes)*60 + int(seconds)
        else:
            spot = time.find(':')
            hours = time[0:spot]
            time = time[spot+1:len(time)]
            spot = time.find(':')
            minutes = time[0:spot]
            seconds = time[spot+1:len(time)]
            return int(hours)*3600 + int(minutes)*60 + int(seconds)

    def test_android_av(self: 'TestAmazon', make_driver: MakeDriver) -> None:
        time.sleep(5)
        d: webdriver.Remote = make_driver("amazon_apple")
        # self.api.lock_device("RFCR90PMZZE")
        # viewer_session_id = self.api.start_session("RFCR90PMZZE@dev-us-pao-5-proxy-27-lin.headspin.io")
        time.sleep(5)
        #splash_page = DiscoveryAndroidSplashPage(d)
        # ts = splash_page.validate_homepage()


        d.execute_script('mobile: pressButton', {'name': 'Select'})
        time.sleep(2)
        d.execute_script('mobile: pressButton', {'name': 'Down'})
        d.execute_script('mobile: pressButton', {'name': 'Down'})
        time.sleep(2)
        d.execute_script('mobile: pressButton', {'name': 'Select'})
        time.sleep(2)
        d.execute_script('mobile: pressButton', {'name': 'Select'})
        time.sleep(5)
        d.execute_script('mobile: pressButton', {'name': 'Up'})
        time.sleep(2)
        searchStartTime = time.time()
        time.sleep(10)
        d.execute_script('mobile: pressButton', {'name': 'Up'})
        time.sleep(2)
        SearchStopTime = time.time()
        time.sleep(4)
        d.execute_script('mobile: pressButton', {'name': 'Select'})

        time.sleep(5)
        # self.api.stop_session(viewer_session_id)
        # self.api.unlock_device("RFCR90PMZZE")

        startLabelID = self.api.ocr_label("First time check", d.session_id, searchStartTime, searchStartTime+2,[[50, 550, 200, 1400]])
        endLabelID = self.api.ocr_label("End time check", d.session_id, SearchStopTime, SearchStopTime+2,[[50, 550, 200, 1400]])

        time.sleep(50)
        logger.info("Waiting for processing")

        startOutput = self.api.get_labels(startLabelID)
        endOutput = self.api.get_labels(endLabelID)

        firstTime = 0
        for label in startOutput['labels']:
            for x in range(len(label['name'])):
                if label['name'][x] == '/':
                    firstTime = label['name'][0:x]

        endTime = 0
        for label in endOutput['labels']:
            print(label['name'])
            for x in range(len(label['name'])):
                if label['name'][x] == '/':
                    endTime = label['name'][0:x]

        firstTime = self.getTime(firstTime)
        endTime = self.getTime(endTime)
        status = "Failure"
        if endTime > firstTime:
            status ="Test Sucess"
            print(firstTime)
            print(endTime)
        Delta = endTime - firstTime
        session_data = {
            "tags": [
                {"status": status},
                {"First Time(s)": firstTime},
                {"End Time(s)": endTime},
                {"Delta(s)": Delta}
            ]
        }
        #self.api.add_tags(viewer_session_id, session_data)
        # self.api.page_load(session_id, ts[0], ts[1])
        #self.api.name_session(session_id, "AV Cold Start Android {}".format(self.date_time), "Test script using appiums python library to mesaure cold start")
TestAmazon.test_android_av('TestAmazon', MakeDriver)