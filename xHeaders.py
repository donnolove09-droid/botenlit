"""Region / endpoint config + the one startup HTTP helper the bot needs.

Cleaned up: the old version started a background thread at import time that
downloaded "tokens" from a third-party Azure site, and contained helpers that
called that site (likes / spam / uid-check) plus sync calls to async functions.
None of it was used by bot.py, so it was removed.
"""
import re
import requests

REGION_CONFIG = {
    "IND": {
        "client_url": "https://client.ind.freefiremobile.com/",
        "server_url": "https://loginbp.ppmainecoonghj.com/",
        "release_version": "OB55",
        "client_version": "1.132.9",
    },
    "AMERICA": {
        "client_url": "https://client.us.freefiremobile.com/",
        "server_url": "https://loginbp.ppmainecoonghj.com/",
        "release_version": "OB55",
        "client_version": "1.132.9",
    },
    "OTHERS": {
        "client_url": "https://clientbp.ppmainecoonghj.com/",
        "server_url": "https://loginbp.ppmainecoonghj.com/",
        "release_version": "OB55",
        "client_version": "1.132.9",
    },
}

REGION_ALIASES = {
    "IND": "IND", "IN": "IND",
    "BR": "AMERICA", "US": "AMERICA", "NA": "AMERICA",
    "SAC": "AMERICA", "AMERICA": "AMERICA",
}


def normalize_region(region):
    key = str(region or "").strip().upper()
    return REGION_ALIASES.get(key, "OTHERS")


def _netloc(url):
    return re.sub(r"^https?://", "", str(url)).split("/")[0]


def client_host(region="OTHERS"):
    return _netloc(REGION_CONFIG[normalize_region(region)]["client_url"])


def client_url(region="OTHERS"):
    return REGION_CONFIG[normalize_region(region)]["client_url"]


def server_url(region="OTHERS"):
    return REGION_CONFIG[normalize_region(region)]["server_url"].rstrip("/")


def client_version(region="OTHERS"):
    return REGION_CONFIG[normalize_region(region)]["client_version"]


def release_version(region="OTHERS"):
    return REGION_CONFIG[normalize_region(region)]["release_version"]


def equie_emote(JWT, url, region="OTHERS"):
    """Best-effort emote equip after login. Never raises."""
    try:
        headers = {
            "Accept-Encoding": "gzip",
            "Authorization": f"Bearer {JWT}",
            "Connection": "Keep-Alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Expect": "100-continue",
            "Host": client_host(region),
            "ReleaseVersion": release_version(region),
            "ClientVersion": client_version(region),
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 13; CPH2095 Build/RKQ1.211119.001)",
            "X-GA": "v1 1",
            "X-Unity-Version": "2018.4.12f1",
        }
        data = bytes.fromhex("CA F6 83 22 2A 25 C7 BE FE B5 1F 59 54 4D B3 13")
        requests.post(f"{str(url).rstrip('/')}/ChooseEmote", headers=headers, data=data, timeout=10)
    except Exception as e:
        print(f"[NEXIO] equie_emote skipped: {e}")
