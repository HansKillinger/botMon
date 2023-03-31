import requests


def get_battle_timers(sessionID, address: str = 'undefinded') -> dict:
    url = f"https://ethermon.io/lite/get_battle_timers?trainer_address={address}"

    _headers = {
        'authority': 'ethermon.io',
        'method': 'GET',
        'path': f'/lite/get_battle_timers?trainer_address={address}',
        'scheme': 'https',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.7',
        'content-type': 'application/json',
        'cookie': f'sessionid={sessionID}',
        'origin': 'https://seasons.ethermon.io',
        'referer': 'https://seasons.ethermon.io/',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Brave";v="110"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Mobile Safari/537.36'
    }
    response = requests.get(url=url)
    return response.json()


def get_rank_all_castles(sessionID, wallet, ladder='ladder1'):
    url = f"https://ethermon.io/lite/ema_battle/get_rank_all_castles?trainer_address={wallet}&ladder_type={ladder}"
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.7",
        "content-type": "application/json",
        "sec-ch-ua": "\"Chromium\";v=\"110\", \"Not A(Brand\";v=\"24\", \"Brave\";v=\"110\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "sec-gpc": "1",
        "cookie": f"sessionid={sessionID}",
        "Referer": "https://seasons.ethermon.io/",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Mobile Safari/537.36'
    }
    payload = {
        "trainer_address": wallet,
        "ladder_type": ladder
    }
    response = requests.get(url=url, headers=headers)
    return response.json()


def attack_battle(sessionID, count, atk_id, def_id, ladder):
    url = "https://ethermon.io/lite/ema_battle/attack_battle"
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "en-US,en;q=0.8",
        "content-type": "application/json",
        "sec-ch-ua": "\"Chromium\";v=\"110\", \"Not A(Brand\";v=\"24\", \"Brave\";v=\"110\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "sec-gpc": "1",
        "cookie": f"sessionid={sessionID}",
        "Referer": "https://seasons.ethermon.io/",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }
    payload = {
        "attack_count": count,
        "attacker_player_id": atk_id,
        "defender_player_id": def_id,
        "ladder_type": ladder
    }
    response = requests.post(url=url, headers=headers, json=payload)
    return response.json()


if __name__ == '__main__':
    pass
