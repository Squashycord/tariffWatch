
from curl_cffi import requests
from datetime import datetime
import time
proxy = None

def get_session(proxy):
    session = requests.Session(
        impersonate="chrome136",
        default_headers=False,
        ja3 = "771,4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53,0-5-10-11-13-16-18-23-27-35-43-45-51-17613-65037-65281,4588-29-23-24,0",
        akamai="1:65536;2:0;4:6291456;6:262144|15663105|0|m,a,s,p",
        extra_fp={
            "tls_signature_algorithms": [
                "ecdsa_secp256r1_sha256",
                "rsa_pss_rsae_sha256",
                "rsa_pkcs1_sha256",
                "ecdsa_secp384r1_sha384",
                "rsa_pss_rsae_sha384",
                "rsa_pkcs1_sha384",
                "rsa_pss_rsae_sha512",
                "rsa_pkcs1_sha512"
            ],
            "tls_grease": True,
            "tls_permute_extensions": True
        },
        verify=False,
        http_version=3 # its actually HTTP/2
    )

    session.proxies = {
        "https": proxy
    }

    return session



def time_ago(date_str):
    # parse ISO string
    dt = datetime.fromisoformat(date_str.replace("Z", "+00:00")).astimezone()  # convert to local tz
    now = datetime.now().astimezone()  # local timezone
    diff = now - dt
    s = diff.total_seconds()
    if s < 60:
        n = int(s)
        unit = "second" if n == 1 else "seconds"
        return f"{n} {unit} ago"
    elif s < 3600:
        n = int(s // 60)
        unit = "minute" if n == 1 else "minutes"
        return f"{n} {unit} ago"
    elif s < 86400:
        n = int(s // 3600)
        unit = "hour" if n == 1 else "hours"
        return f"{n} {unit} ago"
    elif s < 604800:
        n = int(s // 86400)
        unit = "day" if n == 1 else "days"
        return f"{n} {unit} ago"
    elif s < 2592000:
        n = int(s // 604800)
        unit = "week" if n == 1 else "weeks"
        return f"{n} {unit} ago"
    elif s < 31536000:
        n = int(s // 2592000)
        unit = "month" if n == 1 else "months"
        return f"{n} {unit} ago"
    else:
        n = int(s // 31536000)
        unit = "year" if n == 1 else "years"
        return f"{n} {unit} ago"


session = get_session(proxy)


headers = {
    'sec-ch-ua-platform': '"Windows"',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
    'accept': 'application/json, text/plain, */*',
    'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://truthsocial.com/@realDonaldTrump',
    'accept-language': 'en-US,en;q=0.9',
    'priority': 'u=1, i',
}
params = {
    'exclude_replies': 'true',
    'only_replies': 'false',
    'with_muted': 'true',
}
while True:
    response = session.get('https://truthsocial.com/api/v1/accounts/107780257626128497/statuses', params=params, headers=headers)
    data = response.json()
    tariffed = False
    for content in data:
        if "tariff" in content['content'].lower():
            tariffed = True
            break
    if tariffed:
        time_posted = content['created_at']
        how_long_ago = time_ago(time_posted)
        print("President Donald Trump mentioned tarrifs: " + how_long_ago)
        if "hours" in how_long_ago:
            print("\nDonald Trump mentioned tariffs recently, pray for the stock market!\n") 
    else:
        print("President Donald Trump isn't crashing the American stock market. (No tarrifs have been announced recently!)")
    time.sleep(3600)