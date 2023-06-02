from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helpers.userflows import UserFlowAPI
from appium import webdriver
import time
import sys

auth_token='fa2e6312602044678b0d9dd6a41aa01f'
api = UserFlowAPI(auth_token)
userflow = "Check Apps Placement"
description = "test apps placement in Apps area"

#GTV
dc={
    "deviceName": "Chromecast",
    "udid": "27301HFDD7MQGM",
    "automationName": "uiautomator2",
    "appPackage": "com.google.android.apps.tv.launcherx",
    "platformName": "android",
    "appActivity": "com.google.android.apps.tv.launcherx.home.HomeActivity",
    "headspin:controlLock":'true',
    "headspin:capture":"true"
}
print("starting driver")
driver = webdriver.Remote(f"https://dev-ca-tor-0.headspin.io:7031/v0/{auth_token}/wd/hub", dc)
print("starting driver")


# Wait for the GridView to be visible
wait = WebDriverWait(driver, 60)
wait.until(EC.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Logged in as demo@hspin.io, click to choose an account")))



print("The list of installed apps and games in the 'My Apps' area MUST be visible on screen")
print("Expecting: Netflix, YouTube, Prime Video, Disney+")
print("Navigating to 'Apps'")
driver.press_keycode(22)
time.sleep(1)
driver.press_keycode(22)
time.sleep(1)
driver.press_keycode(22)
print("verifying Title")
assert driver.switch_to.active_element.text == 'Apps'
print("navigating to 'My Apps'")

driver.press_keycode(20)
time.sleep(1)
driver.press_keycode(20)


print("Finding Apps")








grid_view = wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, "//android.widget.GridView[@content-desc='Your apps']")))
# Get a list of all child elements of the GridView
child_elements = grid_view.find_elements(AppiumBy.XPATH, ".//*")

# Print the number of child elements found

# Print the text of each child element
x = 0

user_flow_id,response = api.Create_Userflow(userflow, description)
if response.status_code != 200:
    print(f"Error: {response.status_code} - {response.text}")
    sys.exit(1)



for child_element in child_elements:
    if(x==5):
        break

    try:
        assert child_element.tag_name==home_apps[x] and child_element.tag_name != 'None', f"{child_element.tag_name} not in correct spot"
        print("{} in expected place".format(child_element.tag_name))
        x = x+1
    except AssertionError as e:
        print("apps out of order")
        status="failed"
        driver.quit()


print("'My Apps' are in expected order")


status='passed'

if status != "failed":
    status_message = "this session passed"
    response = api.Update_Session(user_flow_id, driver.session_id, status, status_message)
    if response.status_code != 200:
        print(f"Error updating user flow session: {response.status_code} - {response.text}")

driver.quit()