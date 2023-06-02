from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionBuilder
from selenium.webdriver.common.action_chains import ActionChains
from appium.webdriver.extensions.action_helpers import PointerInput
from selenium.webdriver.common.actions import interaction
from os import path
import time
import requests
import json
from helpers.capture import CaptureAPI
from helpers.userflows import UserFlowAPI
import sys
from appium.webdriver.webdriver import ExtensionBase
from apis.hs_apis import HS_API



def perform_action(driver, x, y):
    actions = ActionChains(driver)
    actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
    actions.w3c_actions.pointer_action.move_to_location(x, y)
    actions.w3c_actions.pointer_action.pointer_down()
    actions.w3c_actions.pointer_action.pause(0.1)
    actions.w3c_actions.pointer_action.release()
    actions.perform()




def timer(start, stop):
    elapsed_time = stop - start
    return round(elapsed_time, 2)

userflow = "YT #1"
description = "User should be able to play a youtube video"

movie_title = "First Born"
# GTV Environment
auth_token='fa2e6312602044678b0d9dd6a41aa01f'
api = HS_API(auth_token)

dc={
    "deviceName": "Chromecast",
    "udid": "27301HFDD7MQGM",
    "automationName": "uiautomator2",
    "appPackage": "com.google.android.youtube.tv",
    "platformName": "android",
    "appActivity": "com.google.android.apps.youtube.tv.activity.ShellActivity",
    "headspin:controlLock":'true',
    # "headspin:capture.video":"true"
}
class OCRCommand(ExtensionBase):
    def method_name(self):
        return 'ocr_command'

    def ocr_command(self, argument):
        return self.execute(argument)['value']

    def add_command(self):
        return ('post', '/session/$sessionId/appium/ocr')


driver = webdriver.Remote(f"https://dev-ca-tor-0.headspin.io:7031/v0/{auth_token}/wd/hub", dc, extensions=[OCRCommand])


#STARTAVBOX CAPTURE
capture = CaptureAPI(auth_token)
print("starting capture")
device_id = "R5CR71SM8DT"
capture_id = capture.start_capture(device_id)


print("opening app")
wait = WebDriverWait(driver, 10)

wait.until(EC.visibility_of_element_located((AppiumBy.ID, "android:id/content")))

print("Driver started")

# capture = CaptureAPI(auth_token)
# print("starting capture")
# device_id = "R5CR71SM8DT"
# session_id = capture.start_capture(device_id)
# wait = WebDriverWait(driver, 10)
# start_time=time.time()

time.sleep(5)


#Navigate to Movie
print(f'navigating to {movie_title}')
driver.press_keycode(21);
driver.press_keycode(21);

driver.press_keycode(19);
driver.press_keycode(66);



time.sleep(1)

perform_action(driver, 1142, 200)
perform_action(driver, 878, 278)
perform_action(driver, 1010, 341)
perform_action(driver, 1078, 337)
perform_action(driver, 1142, 341)
perform_action(driver, 892, 473)
perform_action(driver, 869, 200)
perform_action(driver, 814, 332)
perform_action(driver, 1005, 332)
perform_action(driver, 1210, 264)
perform_action(driver, 605, 751)
time.sleep(1)


#Start Movie
start_time=time.time()
print(f'starting {movie_title}')

perform_action(driver, 1694, 951)
time.sleep(30)


#Pause Movie
print(f'pausing {movie_title}')
driver.press_keycode(85)
pause_time = time.time()
print('paused for 30 seconds')
time.sleep(30)


#Write check for fast forward
print('fast forward')
driver.press_keycode(90)
driver.press_keycode(90)
driver.press_keycode(90)
driver.press_keycode(90)
driver.press_keycode(90)
ff = time.time()
driver.press_keycode(85)
driver.press_keycode(85)

#1:05
print('paused for 30 seconds')
# perform_action(driver, 605, 751)
time.sleep(30)


# driver.press_keycode(85)
#Write check for rewind
print('rewind')
driver.press_keycode(89)
driver.press_keycode(89)
driver.press_keycode(89)
driver.press_keycode(89)
ff = time.time()
driver.press_keycode(85)
print('paused for 30 seconds')
driver.press_keycode(85)
# perform_action(driver, 605, 751)
time.sleep(30)




end = time.time()

capture.end_capture(capture_id)
driver.quit()


# ea4334ea-edc1-11ed-93eb-0ad446e63749




# curl -X POST https://fa2e6312602044678b0d9dd6a41aa01f@api-dev.headspin.io/v0/sessions/3e5553da-edc0-11ed-a162-027957d86083/label/add -d '{"labels": [{"name": "Pause Check1", "label_type": "ocr-request", "start_time": 68700, "end_time": 69000, "video_box": [[10, 470, 60, 500]],"data": {"ocr_config": "--psm 9", "confidence_threshold": 30, "target_height": 100}}]}'


# curl https://fa2e6312602044678b0d9dd6a41aa01f@api-dev.headspin.io/v0/sessions/label/1025aef6-edca-11ed-9df5-0615bb030b25/keyframe/start -o start1-screenshot.jpeg



# ea4334ea-edc1-11ed-93eb-0ad446e63749


