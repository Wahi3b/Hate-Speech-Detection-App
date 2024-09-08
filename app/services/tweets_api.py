import requests
import os
import json

bearer_token = os.environ.get("BEARER_TOKEN")


def create_url(user_id):
    
    return "https://api.twitter.com/2/users/{}/tweets".format(user_id)


def get_params():
    return {"tweet.fields" : "text,id,created_at,public_metrics", "max_results" : "5"}

def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserTweetsPython"
    return r

def connect_to_endpoint(url, params):
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()["data"]

def fetch(user_id):
    url = create_url(user_id)
    params = get_params()
    tweets = connect_to_endpoint(url, params)
    return tweets 
