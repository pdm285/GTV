import pytest
import json
import os
import logging
from appium import webdriver
from typing import Callable
from apis.hs_logger import logger, setup_logger
import urllib3
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

setup_logger(logger, logging.DEBUG)

api_token = os.getenv("HS_API_TOKEN")

MakeDriver = Callable[[str], webdriver.Remote]

AMAZON_APPLE_CAPS = {
    "deviceName": "Apple TV 4K",
    "udid": "d22ed6c0d68ce7a828d226ddf03e01fd4e2ee8b7",
    "autoAcceptAlerts": True,
    "platformVersion": "14.4",
    "automationName": "XCUITest",
    "platformName": "tvOS",
    "bundleId": "com.amazon.aiv.AIVApp",
    "headspin:capture.video": True
}

AMAZON_PHONE_CAPS = {
    "deviceName": "iPhone 11",
    "udid": "00008030-001174DE2260402E",
    "automationName": "XCUITest",
    "platformVersion": "14.4",
    "platformName": "iOS",
    "bundleId": "com.amazon.aiv.AIVApp",
    #"headspin:capture.video": True
}
# AMAZON_PHONE_CAPS = {
#     "deviceName": "iPhone 11",
#     "udid": "00008030-001174DE2260402E",
#     "automationName": "XCUITest",
#     "platformVersion": "14.4",
#     "platformName": "iOS",
#     "bundleId": "com.apple.Preferences"
# }

DISCOVERY_ANDROID_CAPS_AV = {
    "deviceName": "iPhone 11",
    "udid": "00008030-001174DE2260402E",
    "automationName": "XCUITest",
    "platformVersion": "14.4",
    "platformName": "iOS",
    "newCommandTimeout": 300,
    "bundleId": "com.amazon.aiv.AIVApp",
}

COMCAST_FIRESTICK_CAP_AV = {
    "deviceName": "AFTMM",
    "udid": "G070VM2414240320",
    "automationName": "UiAutomator2",
    "appPackage": "com.amazon.firetv.youtube",
    "platformName": "Android",
    "appActivity": "dev.cobalt.app.MainActivity"
}

COMCAST_APPLE_CAP_AV = {
    "deviceName": "Apple TV (4th generation)",
    "udid": "3fd3b1ea15a540d684246c25b6708ca9f88eb0ea",
    "automationName": "XCUITest",
    "platformVersion": "15.6",
    "platformName": "tvOS",
    "bundleId": "com.amazon.aiv.AIVApp"
}


@pytest.fixture
def make_driver() -> webdriver.Remote:
    driver = None

    def _make_driver(app: str) -> webdriver.Remote:
        nonlocal driver
        if app == "amazon_apple":
            caps = AMAZON_APPLE_CAPS
            url = "https://dev-us-pao-5.headspin.io:7010/v0/{}/wd/hub".format(api_token)
        elif app == "discovery_android_av":
            caps = DISCOVERY_ANDROID_CAPS_AV
            url = "https://dev-us-pao-5.headspin.io:7046/v0/{}/wd/hub".format(api_token)
        elif app == "comcast_firestick_av":
            caps = COMCAST_FIRESTICK_CAP_AV
            url = "https://dev-ca-tor-0.headspin.io:7026/v0/{}/wd/hub".format(api_token)
        elif app == "comcast_apple_av":
            caps = COMCAST_APPLE_CAP_AV
            url = "https://dev-ca-tor-0.headspin.io:7028/v0/{}/wd/hub".format(api_token)
        elif app == "amazon_phone_ios":
            caps = AMAZON_PHONE_CAPS
            url = "https://dev-ca-tor-0.headspin.io:7028/v0/{}/wd/hub".format(api_token)
        driver = webdriver.Remote(
            command_executor=url,
            desired_capabilities=caps
        )
        logger.info("still in")
        logger.info('\n {}'.format(json.dumps(caps, indent=2)))
        return driver

    yield _make_driver
    driver.quit()