# import pytest




# Step 1: Press Home button
# Step 2: Press Google Assistant button on RCU
# Step 3: Query: “What time is it"
# Step 4: Verify "What time is it" is correctly displayed on the GA window

# 


from time import sleep
from appium import webdriver

runtime = 



single_device = {
    "deviceName": "Chromecast",
    "udid": "22231HFDD54QD9",
    "automationName": "uiautomator2",
    "appPackage": "com.google.android.apps.tv.launcherx",
    "platformName": "android",
    "appActivity": "com.google.android.apps.tv.launcherx.home.HomeActivity",
    "hub_url":"https://dev-us-mv-0.headspin.io:3012/v0/6a4378b310dc4d95b712f5da9ef7accb/wd/hub"
}

if __name__ == "__main__":
    
    


    driver = webdriver.Remote(runtime["hub_url"],runtime)
    driver.launch_app()
    driver.quit()