import requests
import time
from config import Config

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3",
    "x-rapidapi-ua": "RapidAPI-Playground",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site"
}

async def get_key():
    try:
        response = requests.post(
            "https://smailpro.com/app/key",
            json={
                "domain": "gmail.com",
                "username": "random",
                "server": "server-1",
                "type": "alias"
            },
            headers=headers,
            cookies={}
        )
        response.raise_for_status()
        return response.json().get('items')
    except requests.exceptions.RequestException as error:
        print(f"Error: {error}")

async def get_email():
    try:
        key = await get_key()
        response = requests.get(
            f"https://api.sonjj.com/email/gm/get",
            params={
                "key": key,
                "domain": "gmail.com",
                "username": "random",
                "server": "server-1",
                "type": "alias"
            },
            headers=headers
        )
        response.raise_for_status()
        return response.json().get('items')
    except requests.exceptions.RequestException as error:
        print(f"Error: {error}")

async def get_mid(email):
    await delay(10000)
    try:
        key = await get_key()
        response = requests.get(
            f"https://api.sonjj.com/email/gm/check",
            params={
                "key": key,
                'rapidapi-key': 'f871a22852mshc3ccc49e34af1e8p126682jsn734696f1f081',
                "email": email['email'],
                "timestamp": email['timestamp']
            },
            headers=headers
        )
        response.raise_for_status()
        return response.json()['items'][0]['mid']
    except requests.exceptions.RequestException as error:
        print(f"Error: {error}")
        return await get_mid(email)

async def get_message(email):
    try:
        print("Waiting for Email Code...")
        mid = await get_mid(email)
        print("Email Code Received!")
        key = await get_key()
        response = requests.get(
            f"https://api.sonjj.com/email/gm/read",
            params={
                "key": key,
                'rapidapi-key': 'f871a22852mshc3ccc49e34af1e8p126682jsn734696f1f081',
                "email": email['email'],
                "message_id": mid
            },
            headers=headers
        )
        response.raise_for_status()
        security_code_match = re.search(r'>\s*(\d{6})\s*<\/span>', response.text)
        if security_code_match:
            return security_code_match.group(1)
    except requests.exceptions.RequestException as error:
        print(f"Error: {error}")

async def delay(time_ms):
    time.sleep(time_ms / 1000)

# To use the recovery email specified in config.py:
async def get_recovery_email():
    return {"email": Config.RECOVERY_EMAIL}
