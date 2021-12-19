import requests

def send_sms(API_KEY:str="rVOosFCw6bx5fBLXQeDdjm9T7Kn2NAJqpPHZUMtY3vScRh0EGWA8Clhdcb9jIyQEWUrLR6g3FBfwSXHT",numbers="8871117958",msg=""):
    
    url = "https://www.fast2sms.com/dev/bulkV2"

    querystring = {
        "authorization":f"{API_KEY}",
        "message":f"{msg}",
        "language":"english",
        "route":"q",
        "numbers":numbers
    }

    headers = {
        'cache-control': "no-cache"
    }

    response = requests.request(
        "GET", 
        url,
        headers=headers, 
        params=querystring
    )

    return response.text