import requests
import json

class CaptureAPI:
    def __init__(self, auth_token):
        self.auth_token = auth_token

    def lock_device(self, device_id):
        api_endpoint = f"https://api-dev.headspin.io/v0/adb/{device_id}/lock"
        headers = {'Authorization': f'Bearer {self.auth_token}'}
        response = requests.post(api_endpoint, headers=headers)
        response_json = json.loads(response.text)
        return response_json

    def start_capture(self, device_id):
        api_endpoint = "https://@api-dev.headspin.io/v0/sessions"
        headers = {'Authorization': f'Bearer {self.auth_token}'}
        device_data = {"session_type": "capture",
                       "device_address": f"{device_id}@dev-ca-tor-0-proxy-40-lin.headspin.io",
                       "device_id": device_id,
                    #    "capture_video":True,
                       "capture_netrwork": False}
        response = requests.post(api_endpoint, headers=headers, json=device_data)
        response_json = json.loads(response.text)
        session_id = response_json['session_id']
        return session_id

    def end_capture(self, session_id):
        api_endpoint = f"https://api-dev.headspin.io/v0/sessions/{session_id}"
        headers = {'Authorization': f'Bearer {self.auth_token}'}
        device_data = {"active": False}
        response = requests.patch(api_endpoint, auth=(self.auth_token, ""), json=device_data)
        response_json = json.loads(response.text)
        return response_json