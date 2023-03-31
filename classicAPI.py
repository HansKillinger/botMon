import requests


def get_battle_timers(sessionID, address: str = 'undefinded') -> dict:
    url = f"https://ethermon.io/api/get_battle_timers?trainer_address={address}"

    _headers = {
        "accept": "*/*",
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
        "Referer": "https://play.ethermon.io/",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }
    response = requests.get(url=url)
    return response.json()


def get_rank_all_castles(sessionID, wallet, ladder='ladder1'):
    url = f"https://ethermon.io/api/ema_battle/get_rank_all_castles?trainer_address={wallet}&ladder_type={ladder}"
    headers = {
        "accept": "*/*",
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
        "Referer": "https://play.ethermon.io/",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }
    payload = {
        "trainer_address": wallet,
        "ladder_type": ladder
    }
    response = requests.get(url=url, headers=headers)
    return response.json()


def attack_battle(sessionID, count, atk_id, def_id, ladder):
    url = "https://ethermon.io/api/ema_battle/attack_battle"
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
        "Referer": "https://play.ethermon.io/",
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


def claim_all(sessionID, addr):
    url = "https://ethermon.io/api/quest/claim_all"
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
        "Referer": "https://play.ethermon.io/",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }
    payload = {
        "trainer_address": addr
    }
    response = requests.post(url=url, headers=headers, json=payload)
    return response.json()


if __name__ == '__main__':
    pass
