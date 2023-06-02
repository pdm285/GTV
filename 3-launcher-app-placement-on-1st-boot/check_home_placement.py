from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helpers.userflows import UserFlowAPI
import sys
from appium import webdriver
import time
from apis.hs_apis import HS_API

from apis.hs_logger import logger, setup_logger





def getTime(time):
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

userflow = "Check Home Apps Placement"
description = "test apps placement in Home area"

# GTV
auth_token='fa2e6312602044678b0d9dd6a41aa01f'
dc={
    "deviceName": "Chromecast",
    "udid": "27301HFDD7MQGM",
    "automationName": "uiautomator2",
    "appPackage": "com.google.android.apps.tv.launcherx",
    "platformName": "android",
    "appActivity": "com.google.android.apps.tv.launcherx.home.HomeActivity",
    "headspin:controlLock":'true',
    "headspin:capture.video":"true"

}
print("starting driver")

driver = webdriver.Remote(f"https://dev-ca-tor-0.headspin.io:7031/v0/{auth_token}/wd/hub", dc)
print("driver started")

api=HS_API(auth_token)

# Wait for the GridView to be visible
wait = WebDriverWait(driver, 60)


wait.until(EC.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Logged in as demo@hspin.io, click to choose an account")))

print("Checking home apps placement")
print("Expecting: Netflix, YouTube, Prime Video, Disney+")
print("pressing down x1")
driver.press_keycode(20)
time.sleep(1)
print("pressing down x2")
driver.press_keycode(20)
print("pressing down x3")
driver.press_keycode(20)
print("Finding Apps")
time.sleep(1)
searchStartTime = time.time()
time.sleep(5)
searchStopTime = time.time()



driver.quit()


while True:
    status = api.session_done(driver.session_id)
    if status == True:
        break
    time.sleep(15)

yt_coords = [[60, 140, 194, 212]]
prime_coords = [[215,140,310,212]]
Youtube = api.ocr_label("Youtube", driver.session_id, searchStartTime, searchStartTime+5,yt_coords)
Prime = api.ocr_label("Prime Video", driver.session_id, searchStartTime, searchStartTime+5,prime_coords)
startOutput = api.get_labels(Youtube)
groupid = startOutput['labels'][0]['label_group_id']






# curl https://fa2e6312602044678b0d9dd6a41aa01f@api-dev.headspin.io/v0/sessions/label/02b224cc-edcd-11ed-a964-0a8c41cccd51/keyframe/start -o start1-screenshot.jpeg
# curl -X POST https://fa2e6312602044678b0d9dd6a41aa01f@api-dev.headspin.io/v0/sessions/3e5553da-edc0-11ed-a162-027957d86083/label/add -d '{"labels": [{"name": "Youtube", "label_type": "ocr-request", "start_time": 41000, "end_time": 41500, "video_box": [[60, 140, 194, 212]],"data": {"ocr_config": "--psm 7", "confidence_threshold": 30, "target_height": 100}}]}'
# curl -X POST https://fa2e6312602044678b0d9dd6a41aa01f@api-dev.headspin.io/v0/sessions/3e5553da-edc0-11ed-a162-027957d86083/label/add -d '{"labels": [{"name": "Prime Video", "label_type": "ocr-request", "start_time": 41000, "end_time": 41500, "video_box": [[215,140,310,212]],"data": {"ocr_config": "--psm 7", "confidence_threshold": 30, "target_height": 100}}]}'



# api = UserFlowAPI(auth_token)
# user_flow_id,response = api.Create_Userflow(userflow, description)
# if response.status_code != 200:
#     print(f"Error: {response.status_code} - {response.text}")
#     sys.exit(1)

# response = api.Add_Userflow(user_flow_id, driver.session_id)
# if response.status_code != 200:
#     print(f"Error creating user flow session: {response.status_code} - {response.text}")
#     sys.exit(1)
# else:
#     print(f'added to userflow {user_flow_id}')

# status = "passed"
# status_message = "this session passed"
# response = api.Update_Session(user_flow_id, driver.session_id, status, status_message)
# if response.status_code != 200:
#     print(f"Error updating user flow session: {response.status_code} - {response.text}")
