import requests
import json
import traceback
import logging
import datetime
import pytest
import time
import calendar
from datetime import timedelta

from apis.hs_logger import logger, setup_logger

class HS_API():

    start_time = 0
    end_time = 0

    #INTIALIZATION OF APIs WITH HS API TOKEN
    def __init__(self, api_token, device_address=None):
        self.api_token = api_token
        self.url_root = 'https://api-dev.headspin.io/v0/'
        self.headers = {}
        self.headers["Authorization"] = "Bearer {}".format(api_token)
        self.device_address= device_address


    #START A PERFORMANCE SESSION PROGRAMATICALLY
    def start_session(self, device_address):
        request_url = self.url_root + "sessions"
        payload = {}
        payload["session_type"] = "capture"
        payload["device_address"] = device_address
        payload["allow_replace"] = True
        payload["capture_video"] = True
        payload["capture_network"] = False
        payload = json.dumps(payload)
        print("Starting Capture....\n")
        #took out verify here
        response = requests.post(request_url, headers=self.headers, data = payload)
        # print(response.text.encode('utf8'))
        json_data = json.loads(response.text)
        if response.status_code == 200:
            return json_data["session_id"]
        else:
            print("Error starting capture....\n")
            pytest.raises(Exception)

    #STOP A PERFORMANCE SESSION PROGRAMATICALLY
    def stop_session(self, session_id):
        request_url = self.url_root + "sessions/{}".format(session_id)
        payload = "{\"active\": false}"
        #took out verify here
        response = requests.patch(request_url, headers=self.headers, data = payload)
        # print(response.text.encode('utf8'))
        json_data = json.loads(response.text)
        if response.status_code == 200:
            print("Stopped session capture.... {}\n".format(json_data["msg"]))
        else:
            print("Error stopping capture....\n")

    def get_android_device(self, device_id):
        logger.info("Grabbing Android Manufacturer")
        request_url = self.url_root + 'adb/devices'
        #took out verify here
        r = requests.get(request_url, headers=self.headers)
        response = json.loads(r.text)
        for host in response.keys():
            if device_id in host:
                return (response[host].get('model'))

    def get_automation_config(self, device_id):
        print("\n")
        logger.info("Grabbing Automation Config")
        request_url = self.url_root + 'devices/automation-config'
        #took out verify here
        r = requests.get(request_url, headers=self.headers)
        response = json.loads(r.text)
        for host in response.keys():
            if device_id in host:
                return (response[host].get('capabilities'), response[host].get('driver_url'))
        return None

    def upload_results(self, session_id, test_name=None):
        request_url = self.url_root + 'perftests/upload'
        payload = {}
        payload["session_id"] = session_id
        payload["status"] = "passed"
        if test_name != None:
            payload["test_name"] = test_name
        payload = json.dumps(payload)
        #took out verify here
        response = requests.post(request_url, headers=self.headers, data=payload)
        if response.status_code == 200:
            logger.info("Test Uploaded to Userflow")
        else:
            logger.error("Test could not be uploaded: {}".format(response.text))

    def add_tags(self, session_id, tags):
        request_url = self.url_root + 'sessions/tags/{}'.format(session_id)
        payload = json.dumps(tags)
        logger.info(payload)
        #took out verify here
        response = requests.post(request_url, headers=self.headers, data=payload)
        if response.status_code == 200:
            logger.info("Tags Applied")
        else:
            logger.error("Tags could not be applied: {}".format(response.text))

    def adb_shell(self, device_id, command):
        request_url = self.url_root + 'adb/{}/shell'.format(device_id)
        payload = command
        #took out verify here
        response = requests.post(request_url, headers=self.headers, data=payload)
        r = json.loads(response.text)
        if response.status_code == 200:
            return(r["stdout"])
        else:
            logger.error("Could not retrieve adb info")

    def device_info(self, device_id):
        request_url = self.url_root + 'devices'
        #took out verify here
        response = requests.get(request_url, headers=self.headers)
        r = json.loads(response.text)
        if response.status_code == 200:
            entries = r["devices"]
            for i in entries:
                if i["serial"] == device_id:
                    return(i["operator"], i["carriers"])
        else:
            logger.error("Could not device info")

    def page_load(self, session_id, ts_start, ts_end):
        request_url = self.url_root + 'sessions/analysis/pageloadtime/{}'.format(session_id)
        payload = {}
        region_times = []
        start_end = {}
        start_end["name"] = "Cold Start"
        start_end["ts_start"] = ts_start
        start_end["ts_end"] = ts_end
        region_times.append(start_end)
        payload['regions'] = region_times
        payload = json.dumps(payload)
        #took out verify here
        response = requests.post(request_url, headers=self.headers, data = payload)
        if response.status_code == 200:
            logger.info("Cold start calculated with visual page load analysis")
        else:
            logger.error("Cold Start could not be calculated")

    def name_session(self, session_id, name, desc = None):
        request_url = self.url_root + 'sessions/{}/description'.format(session_id)
        payload = {}
        payload["name"] = name
        payload["description"] = name
        payload = json.dumps(payload)
        response = requests.post(request_url, headers=self.headers, data = payload)
        if response.status_code == 200:
            logger.info("Name/Description Added")
        else:
            logger.error("Test could not be named: {}".format(response.text))

    def upload_results(self, session_id, status, test_name=None):
        request_url = self.url_root + 'perftests/upload'
        payload = {}
        payload["session_id"] = session_id
        payload["status"] = status
        if test_name != None:
            payload["test_name"] = test_name
        payload = json.dumps(payload)
        response = requests.post(request_url, headers=self.headers, data=payload)
        if response.status_code == 200:
            logger.info("Test Uploaded to Userflow")
        else:
            logger.error("Test could not be uploaded: {}".format(response.text))

    def lock_device(self, device_id):
        request_url = self.url_root + 'adb/{}/lock'.format(device_id)
        response = requests.post(request_url, headers=self.headers)
        r = json.loads(response.text)
        if response.status_code == 200:
            logger.info("Locking {}".format(device_id))
            return True
        else:
            logger.error("Could not lock device")
            raise Exception("Could not lock {}".format(device_id))

    def unlock_device(self, device_id):
        request_url = self.url_root + 'adb/{}/unlock'.format(device_id)
        response = requests.post(request_url, headers=self.headers)
        r = json.loads(response.text)
        if response.status_code == 200:
            logger.info("Unlocking {}".format(device_id))
            return True
        else:
            logger.error("Could not unlock device")

    def ocr_label_cc(self, name, session_id, startTime, endTime,video_box):
        request_url = self.url_root + 'sessions/{}/label/add'.format(session_id)
        payload = {
            "name": name,
            "label_type": "ocr-request",
            "ts_start": startTime,
            "ts_end": endTime,
            # "start_time": startTime,
            # "end_time": endTime,
            #"video_box":  [[45, 135, 90, 350]],
            "video_box":  video_box,
            "data": {"confidence_threshold": 90, "landscape": True},
            "pinned": True
        }
        payload = json.dumps(payload)
        response = requests.post(request_url, headers=self.headers, data=payload)
        r = json.loads(response.text)
        if response.status_code == 200:
            logger.info("The ocr label is {}".format(r['label_id']))
            return r['label_id']
        else:
            logger.error("The ocr label failed: {}".format(response.text))

        def ocr_label(self, name, session_id, startTime, endTime):
            request_url = self.url_root + 'sessions/{}/label/add'.format(session_id)
        payload = {
            "name": name,
            "label_type": "ocr-request",
            "ts_start": startTime,
            "ts_end": endTime,
            # "start_time": startTime,
            # "end_time": endTime,
            #"video_box":  [[45, 135, 90, 350]],
            "video_box":  [[95, 135, 145, 330]],
            "data": {"confidence_threshold": 70, "landscape": True},
            "pinned": True
        }
        payload = json.dumps(payload)
        response = requests.post(request_url, headers=self.headers, data=payload)
        r = json.loads(response.text)
        if response.status_code == 200:
            logger.info("The ocr label is {}".format(r['label_id']))
            return r['label_id']
        else:
            logger.error("The ocr label failed: {}".format(response.text))

    def get_labels(self, labelID):
        request_url = self.url_root + 'sessions/label/{}'.format(labelID)
        response = requests.get(request_url, headers=self.headers)
        r = json.loads(response.text)
        if response.status_code == 200:
            logger.info("Group Label is {}".format(r['label_group_id']))
            request_url = self.url_root + 'sessions/label/group/{}'.format(r['label_group_id'])
            response = requests.get(request_url, headers=self.headers)
            r = json.loads(response.text)
            if response.status_code == 200:
                logger.info("Found Labels in this group")
                return r
            else:
                logger.error("Nothing found for that group label".format(response.text))
        else:
            logger.error("Could not get group label {}".format(response.text))

    def time_series_label(self, name, session_id, startTime, endTime):
        request_url = self.url_root + 'sessions/{}/label/add'.format(session_id)
        payload = {
            "name": name,
            "label_type": "time-series-request",
            # "ts_start": startTime,
            # "ts_end": endTime,
            "start_time": startTime,
            "end_time": endTime,
            "data": {"method": "range", "time_series_key": "screen_change",
                     "parameters": {"lower_limit": 0.07, "include_lower_limit": True, "duration_threshold_ms": 100, "merge_threshold_ms": 20}},
            "pinned": True
        }
        payload = json.dumps(payload)
        response = requests.post(request_url, headers=self.headers, data=payload)
        r = json.loads(response.text)
        if response.status_code == 200:
            logger.info("The time series label is {}".format(r['label_id']))
            return r['label_id']
        else:
            logger.error("The time series label failed: {}".format(response.text))



    def session_done(self, session_id):
        request_url = self.url_root + \
                      'sessions/analysis/status/{}'.format(session_id) + '?timeout=10'
        response = requests.get(request_url, headers=self.headers)
        r = json.loads(response.text)
        if response.status_code == 200:
            if r["status"] == "done":
                logger.info("Analysis is complete")
                return True
            else:
                logger.error("Analysis is not completed status is ".format(r["status"]))
                return False
        else:
            logger.error("Rest API call failed")
            return False

    def time_series_label_stats(self, name, session_id, startTime, endTime):
        request_url = self.url_root + 'sessions/{}/label/add'.format(session_id)
        payload = {
            "name": name,
            "label_type": "time-series-request",
            # "ts_start": startTime,
            # "ts_end": endTime,
            "start_time": startTime,
            "end_time": endTime,
            "data": {"method": "stats", "time_series_key": "screen_change",
                     "parameters":  {"metrics": ["Mean", "percentile 75"]}},
            "pinned": True
        }
        payload = json.dumps(payload)
        response = requests.post(request_url, headers=self.headers, data=payload)
        r = json.loads(response.text)
        if response.status_code == 200:
            logger.info("The time series label is {}".format(r['label_id']))
            return r['label_id']
        else:
            logger.error("The time series label failed: {}".format(response.text))


    def get_stats(self, session_id):
        request_url = self.url_root + 'sessions/analysis/timeseries/stats/{}'.format(session_id)
        response = requests.get(request_url, headers=self.headers)
        r = json.loads(response.text)
        if response.status_code == 200:
            logger.info("The time series label is {}".format(r))
            return r
        else:
            logger.error("The time series label failed: {}".format(response.text))


