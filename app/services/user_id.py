import requests
import os
import json

bearer_token = os.environ.get("BEARER_TOKEN")

def create_url(user_handle):
    user_fields = "user.fields=id,username,profile_image_url,name,public_metrics"
    url = f"https://api.twitter.com/2/users/by/username/{user_handle}?{user_fields}"
    return url

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserLookupPython"
    return r

def connect_to_endpoint(url):
    response = requests.request("GET", url, auth=bearer_oauth)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()

def user_id(user_handle):
    url = create_url(user_handle)
    json_response = connect_to_endpoint(url)
    # print(json_response)
    return json_response