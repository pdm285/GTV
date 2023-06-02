# import pytest


# 1. Open the Google TV app on an Android smart phone. The phone must be on the same local network that the DUT is.
# 2. Press "Select a device" in the Google TV app
# 3. Verify that the DUT shows up as a device which can be selected 
# 4. Connect to the DUT with the Google TV virtual remote
# 5. Verify that D-pad navigation, Home, Back, Volume Mute, Up, and Down work
# 6. Verify that you can use Google Assistant to send a voice command via the phone app
# 7. Verify that you can alternate between D-pad navigation with Google TV app and DUT remote control successfully
# 8. Verify that you can alternate between Google TV app assistant voice commands and the DUT remote control assistant voice commands successfully
# 9. Verify that, while YouTube is in foreground, voice search using the Google TV app mic function invokes the Google Assistant rather than YouTube's in-app search


from time import sleep
from appium import webdriver

runtime = 



single_device = {
    "deviceName": "Chromecast",
    "udid": "22231HFDD54QD9",
    "automationName": "uiautomator2",
    "platformName": "android",
    "hub_url":"https://dev-us-mv-0.headspin.io:3012/v0/6a4378b310dc4d95b712f5da9ef7accb/wd/hub"
}

if __name__ == "__main__":
    
    


    driver = webdriver.Remote(runtime["hub_url"],runtime)
    driver.launch_app()
    driver.quit()