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


def timer(start, stop):
    return stop - start

userflow = "YT #1"
description = "User should be able to play a youtube video"


# GTV Environment
auth_token='fa2e6312602044678b0d9dd6a41aa01f'
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
driver = webdriver.Remote(f"https://dev-ca-tor-0.headspin.io:7031/v0/{auth_token}/wd/hub", dc)

print("Driver started")

capture = CaptureAPI(auth_token)
print("starting capture")
device_id = "R5CR71SM8DT"
session_id = capture.start_capture(device_id)
wait = WebDriverWait(driver, 10)
start_time=time.time()

#driver.get('https://the-internet.herokuapp.com')
print("opening app")
wait.until(EC.visibility_of_element_located((AppiumBy.ID, "android:id/content")))

print("Opening menu")

driver.back()
actions = ActionChains(driver)
actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
actions.w3c_actions.pointer_action.move_to_location(173, 549)
actions.w3c_actions.pointer_action.pointer_down()
actions.w3c_actions.pointer_action.pause(0.1)
actions.w3c_actions.pointer_action.release()
actions.perform()
    
actions = ActionChains(driver)
actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
actions.w3c_actions.pointer_action.move_to_location(685, 514)
actions.w3c_actions.pointer_action.pointer_down()
actions.w3c_actions.pointer_action.pause(0.1)
actions.w3c_actions.pointer_action.release()
actions.perform()


time.sleep(8)


print("pressing down")
driver.press_keycode(20)
time.sleep(1)

print("pressing down")
driver.press_keycode(20)

print("entering movies with ads")
driver.press_keycode(23)
time.sleep(1)




print("entering movie menu")
driver.press_keycode(23)
time.sleep(1)

print("playing movie")

driver.press_keycode(23)
movie_start = time.time()
print("Watching movie for 120s")
time.sleep(120)
print("finished")
pause_time = time.time()
print('pausing')
driver.press_keycode(85)
time.sleep(30)

driver.press_keycode(90)
driver.press_keycode(90)
driver.press_keycode(90)
driver.press_keycode(90)
time.sleep(30)
ff_time = time.time()

driver.press_keycode(89)
driver.press_keycode(89)
time.sleep(30)
ff_time = time.time()









print("quitting")


driver.quit()
# capture.end_capture(driver.session_id)
# print("ending capture")
# response = capture.end_capture(session_id)
# print(response)


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







