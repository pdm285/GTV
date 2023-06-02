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



def perform_action(driver, x, y):
    actions = ActionChains(driver)
    actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
    actions.w3c_actions.pointer_action.move_to_location(x, y)
    actions.w3c_actions.pointer_action.pointer_down()
    actions.w3c_actions.pointer_action.pause(0.1)
    actions.w3c_actions.pointer_action.release()
    actions.perform()


session_id = ''

class OCRCommand(ExtensionBase):
    def method_name(self):
        return 'ocr_command'

    def ocr_command(self, argument):
        return self.execute(argument)['value']

    def add_command(self):
        return ('post', '/session/$sessionId/appium/ocr'.format(session_id))


def timer(start, stop):
    elapsed_time = stop - start
    return round(elapsed_time, 2)

userflow = "YT #1"
description = "User should be able to play a youtube video"

movie_title = "First Born"
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
    # "headspin:capture.video":"true",
    "headspin:appiumVersion": "2.0.0-beta.52",
    "headspin:appiumPlugins": ["ocr"]
}
driver = webdriver.Remote(f"https://dev-ca-tor-0.headspin.io:7031/v0/{auth_token}/wd/hub", dc, extensions=[OCRCommand])


print("Driver started")
wait = WebDriverWait(driver, 10)
wait.until(EC.visibility_of_element_located((AppiumBy.ID, "android:id/content")))

time.sleep(5)

#Navigate to Movie
print(f'navigating to {movie_title}')
driver.press_keycode(21);
driver.press_keycode(21);

driver.press_keycode(19);list
driver.press_keycode(66);



time.sleep(10)

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



time.sleep(1)

result = driver.ocr_command({})


contexts = driver.contexts
driver.switch_to.context(contexts[1])
try:
    result = driver.find_elements(AppiumBy.XPATH,"//*[contains(text(), 'first born')]")
    x = result[0].location['x']
    y = result[0].location['y']

    perform_action(driver,x,y)
    print(result)
    driver.press_keycode(66)
    timer.sleep(3)
    result=driver.ocr_command({})
except Exception as e:
    print(e)
finally:
    driver.quit()




# curl -X POST https://fa2e6312602044678b0d9dd6a41aa01f@api-dev.headspin.io/v0/sessions/3e5553da-edc0-11ed-a162-027957d86083/label/add -d '{"labels": [{"name": "Pause Check", "label_type": "ocr-request", "start_time": 127000, "end_time": 127500, "video_box": [[18,482,55,500]]}]}'

# curl https://6a4378b310dc4d95b712f5da9ef7accb@api-dev.headspin.io/v0/sessions/label/bf1434cf-99f4-11e9-b9f7-f21898a483e5/keyframe/start -o start-screenshot.jpeg

